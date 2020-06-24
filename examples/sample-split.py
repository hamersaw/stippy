#!/bin/python3
import gdal
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'
    album_id = 'test'
    target_geocode = '9qd9f4'

    # determine album geocode algorithm
    album_geocode = None
    albums = stippy.list_albums(host_addr)
    for album in albums:
        if album.id == album_id:
            album_geocode = album.geocode

    if album_geocode is None:
        print('album geocode algorithm not found')
        exit()

    # iterate over target_geocode substrings (largest to smallest)
    for i in range(0, len(target_geocode)):
        # compute iteration geocode
        geocode = target_geocode[:len(target_geocode) - i]
        print('querying geocode:' + geocode)

        # query single node for Sentinel-2 images with given
        #   iteration geocode and >95% pixel coverage
        stip_iter = stippy.list_node_images(host_addr, album_id,
            min_pixel_coverage=0.95, platform='Sentinel-2', geocode=geocode)

        # process images
        for (node, image) in stip_iter:
            print('  node_id:' + str(node.id) + ' geocode:'
                + image.geocode + ' timestamp:' + str(image.timestamp))

            # find split image dimensions
            min_x, max_x, min_y, max_y = stippy.split_size(
                image.files[0].path, album_geocode, target_geocode)

            split_width = max_x - min_x
            split_height = max_y - min_y

            print('    dimensions:(' + str(split_width)
                + ', ' + str(split_height) + ')')

            # read in base gdal dataset
            dataset = gdal.Open(image.files[0].path)

            # down sample split dataset rasters by a factor of 2
            sample_width = int(split_width / 2)
            sample_height = int(split_height / 2)

            array = dataset.ReadAsArray(xoff=min_x, yoff=min_y,
                xsize=split_width, ysize=split_height,
                buf_xsize=sample_width, buf_ysize=sample_height)

            # if we need to write the resulting arrays out 
            #   to a GeoTiff we can. just to need maintain
            #   dataset projection and geotransform information.
