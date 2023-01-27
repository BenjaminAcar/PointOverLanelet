# lsa-return-lane

## Create the image

Note: The following instructions look weird, you may ask yourself: Why did he not just created a Dockerfile, doing all this? I tried, for some reasons then the lanelet2 library is not working properly. So I had to gone the slow way.

Login to the infra node
```
docker login 
sudo docker run -p 34568:34568 -it --rm majkshkurti/lanelet2 /bin/bash
```
Now create files for the lanelet.py, lanelet2_map.osm and server.py and paste the content of the files inside this repository in the files respectively.
At the end, just run the server.py with
```
python server.py
```

In a second terminal login again to the infra node.

Now find out the container ID with "docker ps" and freeze in the running container image by running:
```
docker commit {<container_id>} lanelet2map
```

Now push that image to the registry:
```
sudo docker login infra.bi.dai-lab.de:5000
docker tag lanelet2map infra.bi.dai-lab.de:5000/lanelet2map
docker push infra.bi.dai-lab.de:5000/lanelet2map
```

If you run a new lanelet2ap container, you can test it with:
```
sudo docker run -p 34568:34568 -it --rm lanelet2map /bin/bash
python server.py
curl -H "lat: 52.5149544484" -H "lon: 13.35700072439" http://localhost:34568/is_over_lanelet
```
Based on our current osm file the output should be the Lanelet ID: 12054.



## Deployment Kubernetes
The deployment is a bit special, because all our pods need to be initialized with the python server.py command, otherwise it will not work.
This is the yaml:
```
apiVersion: apps/v1
kind: Deployment
metadata:
 name: lanelet2map-deployment
 namespace: sensors
 labels:
   app: lanelet2map
spec:
 replicas: 3
 selector:
   matchLabels:
     app: lanelet2map
 template:
   metadata:
     labels:
       app: lanelet2map
   spec:
     imagePullSecrets:
     - name: my-registry-key
     containers:
     - name: lanelet2map
       image: infra.bi.dai-lab.de:5000/lanelet2map
       command: ["python", "~/workspace/server.py"]
       imagePullPolicy: Always
       ports:
       - containerPort: 34568
```

Now just run
```
kubectl apply -f <file.yaml>
```