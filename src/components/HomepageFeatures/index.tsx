import React, { useState } from 'react';
import Map, { NavigationControl,Marker  } from 'react-map-gl/mapbox';
import 'mapbox-gl/dist/mapbox-gl.css';
import styles from './styles.module.css';

// 需要替换为你的Mapbox访问令牌
const MAPBOX_TOKEN = 'pk.eyJ1Ijoia29tb3JlYmkyNzgiLCJhIjoiY203Zm9jYWgyMHJqZDJrb281cWxkaWdwZyJ9.lHT9yV8z2ED5kVbVrOjflw';  // 请替换为你的Mapbox访问令牌

export default function MapComponent(): JSX.Element {
  const [viewState, setViewState] = useState({
    longitude: 0,
    latitude: 20,
    zoom: 1.5
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
              mapStyle="mapbox://styles/mapbox/streets-v11"
              style={{ width: '100%', height: '100%' }}
            >
              <Marker 
                longitude={121.4737} 
                latitude={31.2304} 
                anchor="bottom"
              >
                <div className={styles.markerPin}>
                  <span className={styles.markerLabel}>上海</span>
                </div>
              </Marker>

              <NavigationControl position="top-right" />
              {/* 这里后续可以添加标记个人足迹的Marker组件 */}
            </Map>
          </div>
          <p className={styles.mapDescription}>这是我的世界旅行足迹，每个标记代表一个我曾经到访过的地方。</p>
        </div>
      </div>
    </section>
  );
}
