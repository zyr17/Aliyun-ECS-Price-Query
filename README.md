# Aliyun-ECS-Price-Query
query aliyun ECS prices and find best Preemptible Instance price.

Used to find best price of specified ESC type from all listed regions.

Modify prefer ECS type name and its nickname, and region names, then this script can find 
the lowest price of one type, and its corresponding region.

Sample output:
```
ecs.g5.large            2v8G          cn-huhehaote   0.08856
ecs.c5.large            2v4G          cn-beijing     0.07180
ecs.c6.large            2v4G          cn-shanghai    0.08780
ecs.e5.large            2v4G          cn-wulanchabu  999.00000   // 999 means this type cannot found in all regions.
ecs.ic5.large           2v2G          cn-beijing     0.06880
ecs.g5.xlarge           2v8G          cn-huhehaote   0.16856
ecs.c5.xlarge           4v8G          cn-beijing     0.13380
ecs.c6.xlarge           4v8G          cn-shanghai    0.16580
ecs.ic5.xlarge          4v4G          cn-beijing     0.12780
ecs.gn5-c4g1.xlarge     P100, 4v30G   cn-huhehaote   1.15856
ecs.gn6i-c4g1.xlarge    T4, 4v15G     cn-wulanchabu  1.28020
ecs.gn6e-c12g1.3xlarge  V100, 12v92G  cn-beijing     1.78631
ecs.gn5i-c2g1.large     P4, 2v8G      cn-beijing     1.05140
ecs.gn5i-c4g1.xlarge    P4, 4v16G     cn-beijing     0.97880
ecs.gn6v-c8g1.2xlarge   V100, 8v32G   cn-beijing     1.86200
```
