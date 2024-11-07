
####  3. Build an image
```
docker build  -t dev_image .
```
## DEV
docker run -ti -v $HOME/<localfolder>:/dash --name dash_dev dev_image /bin/bash

