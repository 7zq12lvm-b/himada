    import React, { useState } from 'react';
    import Map, { NavigationControl, Marker } from 'react-map-gl/mapbox';
    import 'mapbox-gl/dist/mapbox-gl.css';
    import styles from './styles.module.css';
    import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
    import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
    import { cities } from './data'

    // 需要替换为你的Mapbox访问令牌
    const MAPBOX_TOKEN = 'pk.eyJ1Ijoia29tb3JlYmkyNzgiLCJhIjoiY204ZjgxMjR6MGF1MzJrczVvd3M0dGZrdCJ9.JbRKakNbEmRy0Z_nLcc7Cg';  // 请替换为你的Mapbox访问令牌

    function MapComponent() {
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
    };

    export default MapComponent;