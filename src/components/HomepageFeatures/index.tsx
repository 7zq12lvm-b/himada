import React, { useState } from 'react';
import Map, { NavigationControl,Marker  } from 'react-map-gl/mapbox';
import 'mapbox-gl/dist/mapbox-gl.css';
import styles from './styles.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';


// 需要替换为你的Mapbox访问令牌
const MAPBOX_TOKEN = 'pk.eyJ1Ijoia29tb3JlYmkyNzgiLCJhIjoiY203Zm9jYWgyMHJqZDJrb281cWxkaWdwZyJ9.lHT9yV8z2ED5kVbVrOjflw';  // 请替换为你的Mapbox访问令牌
// 城市坐标数据
const cities = [
  { name: '廊坊', longitude: 116.7064, latitude: 39.5180 },
  { name: '北京', longitude: 116.3912, latitude: 39.9060 },
  { name: '天津', longitude: 117.2010, latitude: 39.0842 },
  { name: '衡水', longitude: 115.6864, latitude: 37.7392 },
  { name: '沧州', longitude: 116.8578, latitude: 38.3106 },
  { name: '张家口', longitude: 114.8872, latitude: 40.8231 },
  { name: '呼和浩特', longitude: 111.7490, latitude: 40.8416 },
  { name: '洛阳', longitude: 112.4540, latitude: 34.6197 },
  { name: '西宁', longitude: 101.7787, latitude: 36.6176 },
  { name: '济南', longitude: 117.1201, latitude: 36.6512 },
  { name: '青岛', longitude: 120.3825, latitude: 36.0671 },
  { name: '泰安', longitude: 117.1290, latitude: 36.1944 },
  { name: '无锡', longitude: 120.3016, latitude: 31.5728 },
  { name: '南京', longitude: 118.7969, latitude: 32.0603 },
  { name: '杭州', longitude: 120.2052, latitude: 30.2526 },
  { name: '苏州', longitude: 120.5853, latitude: 31.2989 },
  { name: '九江', longitude: 116.0019, latitude: 29.7051 },
  { name: '厦门', longitude: 118.0894, latitude: 24.4798 },
  { name: '广州', longitude: 113.2644, latitude: 23.1291 },
  { name: '深圳', longitude: 114.0579, latitude: 22.5431 },
  { name: '海口', longitude: 110.1998, latitude: 20.0444 },
  { name: '三亚', longitude: 109.5120, latitude: 18.2524 },
  { name: '长沙', longitude: 112.9823, latitude: 28.1941 },
  { name: '南昌', longitude: 115.8531, latitude: 28.6859 },
  { name: '开封', longitude: 114.2766, latitude: 34.7963 },
  { name: '长治', longitude: 113.1163, latitude: 36.1954 },
  { name: '大同', longitude: 113.3001, latitude: 40.0768 },
  { name: '西安', longitude: 108.9402, latitude: 34.3416 },
  { name: '成都', longitude: 104.0667, latitude: 30.6667 },
  { name: '雅安', longitude: 103.0010, latitude: 29.9877 },
  { name: '康定', longitude: 101.9641, latitude: 30.0585 },
  { name: '昌都', longitude: 97.1785, latitude: 31.1369 },
  { name: '林芝', longitude: 94.3624, latitude: 29.6486 },
  { name: '拉萨', longitude: 91.1119, latitude: 29.6625 },
  { name: '哈尔滨', longitude: 126.6433, latitude: 45.7563 },
  { name: '七台河', longitude: 131.0033, latitude: 45.7705 },
  { name: '海参崴', longitude: 131.8869, latitude: 43.1198 }, // 俄罗斯城市
  { name: '冲绳那霸', longitude: 127.6791, latitude: 26.2130 } // 日本城市
];
export default function MapComponent(): JSX.Element {
  const [viewState, setViewState] = useState({
    longitude: 75.9898,
    latitude: 39.4704,
    zoom: 3
  });

  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.mapContainer}>
          <h2 className={styles.mapTitle}>我的足迹地图</h2>
          <div className={styles.mapWrapper}>
            <Map
              mapboxAccessToken={MAPBOX_TOKEN}
              initialViewState={viewState}
              onMove={evt => setViewState(evt.viewState)}
              mapStyle="mapbox://styles/mapbox/streets-v11?language=zh"
              locale={{ 'NavigationControl.ZoomIn': '放大', 'NavigationControl.ZoomOut': '缩小' }}  // 控件翻译
              style={{ width: '100%', height: '100%' }}
            >
              {cities.map((city, index) => (
                <Marker 
                  key={index}
                  longitude={city.longitude} 
                  latitude={city.latitude}
                  anchor="bottom"
                  popup={{
                    closeButton: false,
                    closeOnClick: true,
                    content: city.name
                  }}
                >
                  <div className={styles.markerTooltip}>
                    <FontAwesomeIcon 
                      icon={faMapMarkerAlt} 
                      size="lg" 
                      style={{ color: "#f70202" }} 
                    />
                    <span className={styles.tooltipText}>{city.name}</span>
                  </div>
                </Marker>
              ))}
              <NavigationControl position="top-right" />
            </Map>
          </div>
          {/* <p className={styles.mapDescription}>这是我的世界旅行足迹，每个标记代表一个我曾经到访过的地方。</p> */}
        </div>
      </div>
    </section>
  );
}
