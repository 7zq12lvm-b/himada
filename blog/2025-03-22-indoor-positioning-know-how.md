---
slug: indoor-positioning-know-how
title: neXenio/BLE-Indoor-Positioning库的定位策略
authors: mingqiang
tags: [indoor positioning, bluetooth]
---

# Java 库定位策略分析

您的总结大体正确，但需要一些修正和细节补充。以下是 Java 库中定位策略的更完整描述：

## Java 库的定位策略

### 1. 数据收集阶段
- 系统收集最近 60 秒内的 Beacon 广播包数据：
  ```java
  public static final long MAXIMUM_PACKET_AGE = TimeUnit.SECONDS.toMillis(60);
  ```
- 但实际上只会使用最近 2 秒内活跃的 Beacon：
  ```java
  if (!beacon.hasBeenSeenInThePast(2, TimeUnit.SECONDS)) {
      return false; // beacon hasn't been in range recently, avoid using outdated data
  }
  ```

### 2. 信号处理阶段
- 系统对每个 Beacon 的 RSSI 信号进行平滑处理，默认采用 **Kalman 滤波**：
  ```java
  public WindowFilter createSuggestedWindowFilter() {
      return new KalmanFilter(getLatestTimestamp());
  }
  ```
  
- Kalman 滤波器会处理每个 Beacon 最近接收到的 RSSI 值，考虑测量噪声和过程噪声：
  ```java
  float measurementNoise = AdvertisingPacketUtil.calculateVariance(rssiArray);
  float processNoise = PROCESS_NOISE_DEFAULT; // 通常设为 0.008
  ```

- 而不是简单地取平均值。对于每个 Beacon，都会基于时间窗口内的一系列 RSSI 值计算出一个平滑后的 RSSI 值。

### 3. 距离计算阶段
- 系统根据平滑后的 RSSI 值，使用对数距离路径损耗模型计算距离：
  ```java
  public static float calculateDistance(float rssi, float calibratedRssi, float pathLossParameter) {
      return (float) Math.pow(10, (calibratedRssi - rssi) / (10 * pathLossParameter));
  }
  ```

- 路径损耗参数根据环境不同有差异：
  ```java
  public static final float PATH_LOSS_PARAMETER_OPEN_SPACE = 2;
  public static final float PATH_LOSS_PARAMETER_INDOOR = 1.7f;
  public static final float PATH_LOSS_PARAMETER_OFFICE_HARD_PARTITION = 3f;
  ```

### 4. Beacon 选择和过滤阶段
- 系统会排序可用的 Beacon，优先使用 RSSI 信号更强的 Beacon：
  ```java
  Collections.sort(usableBeacons, BeaconUtil.DescendingRssiComparator);
  ```

- 限制使用的 Beacon 数量在合理范围内：
  ```java
  private static final int MINIMUM_BEACON_COUNT = 3; // 至少需要3个
  private static final int MAXIMUM_BEACON_COUNT = 10; // 最多使用10个
  ```

- 过滤掉信号过弱的 Beacon：
  ```java
  if (usableBeacons.get(beaconIndex).getFilteredRssi() < minimumRssiThreshold) {
      firstRemovableBeaconIndex = beaconIndex;
      break;
  }
  ```

### 5. 位置计算阶段
- 系统使用 **多边测量算法** (Multilateration) 而非简单的三点定位：
  ```java
  Multilateration multilateration = new Multilateration(usableBeacons);
  try {
      Location location = multilateration.getLocation();
      // ...
  }
  ```

- 多边测量基于最小二乘法优化，使用 Levenberg-Marquardt 算法：
  ```java
  TrilaterationFunction trilaterationFunction = new TrilaterationFunction(positions, distances);
  LeastSquaresOptimizer leastSquaresOptimizer = new LevenbergMarquardtOptimizer();
  NonLinearLeastSquaresSolver solver = new NonLinearLeastSquaresSolver(trilaterationFunction, leastSquaresOptimizer);
  ```

- 系统还会根据均方根误差 (RMS) 过滤掉不准确的位置估计：
  ```java
  if (multilateration.getRMS() < rootMeanSquareThreshold) {
      locationPredictor.addLocation(location);
      onLocationUpdated(location);
  }
  ```

### 6. 位置优化阶段
- 系统使用 LocationPredictor 来预测未来位置：
  ```java
  locationPredictor.addLocation(location);
  ```

- 还应用了移动速度限制：
  ```java
  if (maximumMovementSpeed != MAXIMUM_MOVEMENT_SPEED_NOT_SET && lastKnownLocation != null) {
      location = DistanceUtil.speedFilter(lastKnownLocation, location, maximumMovementSpeed);
  }
  ```

### 7. 更新频率
- 默认位置更新频率为每 500 毫秒一次：
  ```java
  private long maximumLocationUpdateInterval = UPDATE_INTERVAL_MEDIUM; // 500ms
  ```
  
- 但可以配置为其他值：
  ```java
  public static final long UPDATE_INTERVAL_IMMEDIATE = 50;    // 50ms
  public static final long UPDATE_INTERVAL_FAST = 100;        // 100ms
  public static final long UPDATE_INTERVAL_MEDIUM = 500;      // 500ms
  public static final long UPDATE_INTERVAL_SLOW = 3000;       // 3000ms
  ```

## 总结比较

与您的描述相比，主要差异点：

1. **信号处理**: 不是简单取平均值，而是使用 Kalman 滤波器处理 RSSI 值
2. **位置计算**: 不仅使用三点定位，而是使用多边测量算法，可以同时考虑 3 个以上的 Beacon
3. **精度控制**: 使用 RMS 阈值过滤掉不准确的定位结果
4. **预测优化**: 使用位置预测和速度限制来平滑结果

当前您的前端代码已经实现了一些这些技术（如 Kalman 滤波），但可以考虑更全面地引入 Java 库中的高级功能，特别是多边测量算法和位置预测方面。