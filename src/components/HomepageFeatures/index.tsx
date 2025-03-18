import React, { useState } from 'react';
import Map, { NavigationControl,Marker  } from 'react-map-gl/mapbox';
import 'mapbox-gl/dist/mapbox-gl.css';
import styles from './styles.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';


// 需要替换为你的Mapbox访问令牌
const MAPBOX_TOKEN = 'pk.eyJ1Ijoia29tb3JlYmkyNzgiLCJhIjoiY203Zm9jYWgyMHJqZDJrb281cWxkaWdwZyJ9.lHT9yV8z2ED5kVbVrOjflw';  // 请替换为你的Mapbox访问令牌

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
            <Marker 
              longitude={121.4737} 
              latitude={31.2304}
              anchor="bottom"
            >
                <FontAwesomeIcon 
                  icon={faMapMarkerAlt} 
                  size="2x" 
                  style={{color: "#f70202",}} 
                  />
            </Marker>

            <NavigationControl position="top-right" />
              {/* 这里后续可以添加标记个人足迹的Marker组件 */}
            </Map>
          </div>
          {/* <p className={styles.mapDescription}>这是我的世界旅行足迹，每个标记代表一个我曾经到访过的地方。</p> */}
        </div>
      </div>
    </section>
  );
}
