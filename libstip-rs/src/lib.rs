use cpython::{PyErr, PyResult, Python};
use cpython::exc::{IOError, NotImplementedError};
use failure::ResultExt;
use gdal::raster::Dataset;
use st_image::prelude::{DatasetSplit, Geocode};

use std::error::Error;
use std::path::PathBuf;

// add bindings to the generated python module
cpython::py_module_initializer!(libstiprs, |py, m| {
    m.add(py, "__doc__", "")?;
    m.add(py, "split_size", cpython::py_fn!(py, split_size_py(
        path_str: &str, geocode: u16, target_geocode: &str)))?;
    Ok(())
});

fn split_size_py(py: Python, path_str: &str, geocode: u16,
        target_geocode: &str) -> PyResult<(isize, isize, isize, isize)> {
    // compile Geocode algorithm
    let geocode = match geocode {
        0 => Geocode::Geohash,
        1 => Geocode::QuadTile,
        _ => return Err(PyErr::new::<NotImplementedError, String>(py,
            format!("geocode algorithm '{}' does not exist", geocode))),
    };

    // check if path exists
    let path = PathBuf::from(path_str);
    if !path.exists() {
        return Err(PyErr::new::<IOError, String>(py,
            format!("image path '{}' does not exist",
                path.to_string_lossy())));
    }

    // open dataset
    let dataset = match Dataset::open(&path).compat() {
        Ok(dataset) => dataset,
        Err(e) => return Err(PyErr::new::<IOError, String>(py,
            format!("failed to open dataset: {}", e))),
    };

    // split dataset
    let option = match split(&dataset, geocode, target_geocode) {
        Ok(option) => option,
        Err(e) => return Err(PyErr::new::<IOError, String>(py,
            format!("failed to split dataset: {}", e))),
    };

    let dataset_split = match option {
        Some(dataset) => dataset,
        None => return Err(PyErr::new::<IOError, String>(py,
            format!("geocode split does not exist"))),
    };

    // return coordinates
    let (min_x, max_x, min_y, max_y) = dataset_split.pixels();
    Ok((min_x, max_x, min_y, max_y))
}

fn split<'a>(dataset: &'a Dataset, geocode: Geocode, target_geocode: &str)
        -> Result<Option<DatasetSplit<'a>>, Box<dyn Error>> {
    // split image with geocode precision
    for dataset_split in st_image::prelude::split(
            dataset, geocode, target_geocode.len())? {
        // calculate split dataset geocode
        let (win_min_x, win_max_x, win_min_y, win_max_y) =
            dataset_split.coordinates();
        let split_geocode = geocode.get_code(
            (win_min_x + win_max_x) / 2.0,
            (win_min_y + win_max_y) / 2.0, target_geocode.len())?;

        // check this split is the correct target geocode 
        if target_geocode != split_geocode {
            continue;
        }

        // return dataset
        return Ok(Some(dataset_split));
    }

    Ok(None)
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
