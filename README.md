This code is used, to determine whether a certain point is over a lanelet or not. The lanelets are provided by a osm file.

Note: The following instructions look weird, you may ask yourself: Why did he not just created a Dockerfile, doing all this? I tried, for some reasons then the lanelet2 library is not working properly. So I had to gone the slow way.

First, create a Docker container with the lanelet library installed.
```
sudo docker run -p 34568:34568 -it --rm majkshkurti/lanelet2 /bin/bash
```
Now create files for the lanelet.py, lanelet2_map.osm and server.py and paste the content of the files inside this repository in the created files respectively. For the lanelet2_map.osm file put the osm data of your map inside.

At the end, just run the server.py with
```
python server.py
```

The server.py contains the code for running a server. By sending requests to the server, the functionality can be triggered. The code to check whether the point is over a lanelet or not is in lanelet.py.

You can test the code with the following command
```
curl -H "lat: 52.5149544484" -H "lon: 13.35700072439" http://localhost:34568/is_over_lanelet
```
Depending on your lat/long and your osm file, an lanelet ID will be returned, or not.




Note: The MercatorProjector is used to translate the lat/lon coordinates to the internal coordinates of the lanelet library. For some reasons lanelet is not using UTM, like expected. Therefore we used the MercatorProjector projection.
