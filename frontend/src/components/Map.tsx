import {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapMarker, reactify, YMapDefaultMarker, YMapFeature} from './lib/ymap';
import { useEffect, useState, useCallback } from "react";
import {fetchRoute} from '../helpers/fetchRoute';
// import type {YMapLocationRequest} from 'ymaps3';

const LOCATION = {
  center: [37.588144, 55.733842],
  zoom: 9
};

const LINE_STYLE = {
  simplificationRate: 0,
  stroke: [
    {width: 7, color: '#83C753'},
    {width: 9, color: '#000000', opacity: 0.3}
  ]
};

const coordsHopper =  [[
  73.368071,
  54.991923
],
[
  73.36838,
  54.991921
],
[
  73.368729,
  54.991913
],
[
  73.368753,
  54.992501
],
[
  73.370549,
  54.992469
],
[
  73.370554,
  54.992547
],
[
  73.372203,
  54.992513
],
[
  73.372282,
  54.993105
],
[
  73.37332,
  54.993076
],
[
  73.3748,
  54.992992
],
[
  73.374904,
  54.992972
],
[
  73.375298,
  54.992834
],
[
  73.375936,
  54.99345
],
[
  73.376019,
  54.993502
],
[
  73.376481,
  54.993936
],
[
  73.376443,
  54.993947
],
[
  73.376612,
  54.994153
],
[
  73.376657,
  54.994146
],
[
  73.377023,
  54.994467
],
[
  73.377077,
  54.994487
],
[
  73.377188,
  54.994446
],
[
  73.378976,
  54.996086
],
[
  73.379733,
  54.995815
],
[
  73.380627,
  54.996637
],
[
  73.381463,
  54.996338
],
[
  73.381814,
  54.996661
],
[
  73.383452,
  54.996075
],
[
  73.384689,
  54.997264
],
[
  73.384843,
  54.997209
],
[
  73.386017,
  54.996785
],
[
  73.38615,
  54.996787
],
[
  73.386397,
  54.996815
],
[
  73.386687,
  54.996872
],
[
  73.3878,
  54.99721
],
[
  73.388277,
  54.99734
],
[
  73.388626,
  54.997527
],
[
  73.388678,
  54.997572
],
[
  73.388845,
  54.997563
],
[
  73.388963,
  54.997573
],
[
  73.389506,
  54.997752
],
[
  73.389881,
  54.997865
],
[
  73.391312,
  54.998206
],
[
  73.391463,
  54.998313
],
[
  73.391342,
  54.998348
],
[
  73.391145,
  54.998528
],
[
  73.391839,
  54.999158
],
[
  73.392506,
  54.999798
]
]

const dataRes3 = {
  geometry: {
    type: 'LineString',
    coordinates: coordsHopper,
  },
  style: {
    stroke: [{width: 12, color: 'rgb(14, 194, 219)'}]
  }

}



const CustomMap = ({routeArr,  ...props}: {routeArr: any[]}) => {
    const [route, setRoute] = useState(routeArr);

    const handleRoute = useCallback((route) => {
        if (route){
            setRoute(route);
        } else {
            setRoute(null);
        }
    }, [routeArr]);
    useEffect(() => {
    }, [])
    console.log('geo:', routeArr)
    
  return (
    <div style={{width: '100%', height: '400px'}}>
      <YMap location={reactify.useDefault(LOCATION)}>
        <YMapDefaultSchemeLayer />
        <YMapDefaultFeaturesLayer />
        <YMapDefaultSchemeLayer />
              {/* Add route start and end markers to the map */}
              <>
              {/* <YMapMarker key={[24, 23]} coordinates={reactify.useDefault(item.coords)} draggable={false}>
                    <h2>Hello</h2>
                </YMapMarker> */}
              {(routeArr ?? []).map((item) => (
                <YMapMarker coordinates={reactify.useDefault(item)} draggable={false}>
                    <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    >
                    <line
                        x1="12"
                        y1="2"
                        x2="12"
                        y2="16"
                        stroke="black"
                        strokeWidth="2"
                        strokeLinecap="round"
                    />
                    <circle cx="12" cy="20" r="2" fill="black" />
                    </svg>
                    </YMapMarker>
                // </YMapDefaultMarker>
                ))}
              </>
              {/* {route && <YMapFeature {...dataRes2} style={LINE_STYLE} 
              disableRoundCoordinates={false}
              />} */}
              {/* <YMapDefaultMarker
                coordinates={routeArr[0]}
                title="Point A"
                draggable
                size="normal"
                iconName="fallback"
                
              />
              <YMapDefaultMarker
                coordinates={routeArr[1]}
                title="Point B"
                draggable
                size="normal"
                iconName="fallback"
                
              /> */}

              {/* Add the route line to the map when it becomes available */}
      </YMap>
    </div>
  );
}

export default CustomMap;