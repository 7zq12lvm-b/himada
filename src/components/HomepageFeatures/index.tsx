import MapComponent from './map';
import 'mapbox-gl/dist/mapbox-gl.css';

export default function Index(): JSX.Element {

  return (
      <div className="indexDiv">
        <MapComponent/>
      </div>
  );
}
