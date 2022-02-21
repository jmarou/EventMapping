import {renderToString} from "react-dom/server";
import { useHistory } from "react-router-dom";
import React from "react";
import axios from "axios";
import file from "./file.json";
import blueIconpng from "./blueIcon.png";
import redIconpng from "./redIcon.png";
import "leaflet-easybutton";
import "leaflet-easybutton";
import "./App.css";

// import { Col, Row, Container } from "react-bootstrap";
// import JSON from "json";
// import * as L from "leaflet/dist/leaflet";

let police_tweets;
let pyrosvestiki_tweets;

// This line takes leaflet from the index.html declaration
let L = window.L;

let LeafletMap = (props) => {
  let history = useHistory();
  let [mapState, setMapState] = React.useState();

  React.useEffect(() => {
    const home = {
      lat: 38.505,
      lng: 23.91,
      zoom: 6.5,
    };
    const OpenStreetMap = L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }
    );

    const Google_Satellite = L.tileLayer(
      "http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        subdomains: ["mt0", "mt1", "mt2", "mt3"],
      }
    );

    const OpenTopoMap = L.tileLayer(
      "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
      }
    );

    const HumanitarianMap = L.tileLayer(
      "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          "© OpenStreetMap Contributors. Tiles courtesy of Humanitarian OpenStreetMap Teams",
      }
    );
    const WaterColorMap = L.tileLayer(
      // "http://c.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
      "https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>',
      }
    );

    const TonerMap = L.tileLayer(
      // "http://c.tile.stamen.com/watercolor/${z}/${x}/${y}.jpg",
      "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
      }
    );

    let map = new L.map("mapid", { zoomControl: false, cursor: true });
    map.setView([home.lat, home.lng], home.zoom, false);

    TonerMap.addTo(map);

    const basemaps = {
      OpenStreetMap: OpenStreetMap,
      HumanitarianMap: HumanitarianMap,
      "Toner Map": TonerMap,
      OpenTopoMap: OpenTopoMap,
      "Water Color Map": WaterColorMap,
      "Google Satellite": Google_Satellite,
    };
    const blueIcon = L.icon({
      iconUrl: blueIconpng,
      shadowUrl:
        "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -34],
      shadowAnchor: [13, 40],
    });

    const redIcon = L.icon({
      iconUrl: redIconpng,
      shadowUrl:
        "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -34],
      shadowAnchor: [13, 40],
    });

    // TEST
    // let testmarker = L.marker([38.2, 23.23])
    // .bindPopup(
    //   // `<blockquote class="twitter-tweet" data-theme="dark"><p lang="el" dir="ltr">❗Περισσότερα από 67 κιλά κάνναβης κατασχέθηκαν από αστυνομικούς της Διεύθυνσης Αστυνομίας Ορεστιάδας σε παρέβρια περιοχή του Έβρου.<br>👉<a href="https://t.co/K4MkPuiAVI">https://t.co/K4MkPuiAVI</a> <a href="https://t.co/zVLMGR2VCC">pic.twitter.com/zVLMGR2VCC</a></p>&mdash; Ελληνική Αστυνομία (@hellenicpolice) <a href="https://twitter.com/hellenicpolice/status/1494387434112655362?ref_src=twsrc%5Etfw">February 17, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> `
    //   `<blockquote class="twitter-tweet"><p lang="el" dir="ltr"><a href="https://twitter.com/hellenicpolice/status/1494387434112655362?ref_src=twsrc%5Etfw">February 17, 2022</a></blockquote>`
    // )
    // .addTo(map);

    // console.log(file);
    // var layer1 = L.geoJson(file, {
    //       pointToLayer: function (feature, latlng) {
    //         return L.marker(latlng, {icon: redIcon});
    //       } ,
    //       onEachFeature: function (feature, layer, latlng) {
    //         layer.bindPopup(
    //           renderToString(
    //             <div>
    //               <h1>Tweet</h1>
    //               {/* <a href={"https://twitter.com/pyrosvestiki/status/"+ feature.properties.id}>Tweet</a> */}
    //               <h3><strong>Id</strong> = {feature.properties.id}</h3>
    //               <h3><strong>Created At</strong> = {Date(feature.properties.created_at).split(' ').slice(0,5).join(' ')}</h3>
    //               <h3><strong>Location</strong> = [{feature.geometry.coordinates[0]},{feature.geometry.coordinates[1]}]</h3>
    //               <h3><strong>Text</strong></h3>
    //               <h3>{feature.properties.text}</h3>
    //            </div>
    //           )
    //         );
    //     }
    // }).addTo(map);
    // layer1.setStyle({redIcon});

    axios.get("/GetLayer_Police").then(function (response) {
      console.log(response.data);
      police_tweets = L.geoJson(file, {
        pointToLayer: function (feature, latlng) {
          return L.marker(latlng, { icon: blueIcon });
        },
        onEachFeature: function (feature, layer, latlng) {
          layer.bindPopup(
            renderToString(
              <div>
                <h2>Hellenic Police Tweet</h2>
                {/* <h1><a href="https://twitter.com/pyrosvestiki/status/{feature.properties.id}" Tweet></a></h1> */}
                <h3>
                  <strong>Id</strong> = {feature.properties.id}
                </h3>
                <h3>
                  <strong>Created At</strong> ={" "}
                  {Date(feature.properties.created_at)
                    .split(" ")
                    .slice(0, 5)
                    .join(" ")}
                </h3>
                <h3>
                  <strong>Location</strong> = [{feature.geometry.coordinates[0]}
                  ,{feature.geometry.coordinates[1]}]
                </h3>
                <h4>
                  <strong>Text</strong>
                </h4>
                <h3>{feature.properties.text}</h3>
              </div>
            )
          );
        },
      });

      axios.get("/GetLayer_Pyrosvestiki").then(function (response) {
        // console.log(response.data);
        pyrosvestiki_tweets = L.geoJson(file, {
          pointToLayer: function (feature, latlng) {
            return L.marker(latlng, { icon: redIcon });
          },
          onEachFeature: function (feature, layer, latlng) {
            layer.bindPopup(
              renderToString(
                <div>
                  <h1>Hellenic Fire Department Tweet</h1>
                  {/* <h1><a href="https://twitter.com/pyrosvestiki/status/{feature.properties.id}" Tweet></a></h1> */}
                  <h3>
                    <strong>Id</strong> = {feature.properties.id}
                  </h3>
                  <h3>
                    <strong>Created At</strong> ={" "}
                    {Date(feature.properties.created_at)
                      .split(" ")
                      .slice(0, 5)
                      .join(" ")}
                  </h3>
                  <h3>
                    <strong>Location</strong> = [
                    {feature.geometry.coordinates[0]},
                    {feature.geometry.coordinates[1]}]
                  </h3>
                  <h3>
                    <strong>Text</strong>
                  </h3>
                  <h3>{feature.properties.text}</h3>
                </div>
              )
            )
          }
        });

        pyrosvestiki_tweets.addTo(map);

        const overlaymaps = {
          "Tweets: Hellenic Fire Department": pyrosvestiki_tweets,
          // "Tweets: Hellenic Police": police_tweets,
        };
        L.control.layers(basemaps, overlaymaps).addTo(map);
      });

    });

    L.control.zoom({ position: "topleft" }).addTo(map);

    map.setMaxBounds(map.getBounds());

    L.easyButton(
      "fa-home",
      function (btn, map) {
        map.setView([home.lat, home.lng], home.zoom);
      },
      "Initial View"
    ).addTo(map);

    let Position = L.Control.extend({
      _container: null,
      options: {
        position: "bottomleft",
      },

      onAdd: function (map) {
        var latlng = L.DomUtil.create("div", "mouseposition");
        this._latlng = latlng;
        return latlng;
      },

      updateHTML: function (lat, lng) {
        this._latlng.innerHTML = "lat: " + lat + " lon: " + lng;
        this._latlng.style.border = "2px solid #777";
        this._latlng.style.borderTop = "none";
        this._latlng.style.background = "rgba(255,255,255,0.5)";
        this._latlng.style.padding = "0px 5px 0px";
        this._latlng.style.left = "-3%";
        this._latlng.style.marginTop = "-2.5%";
      },
    });

    let position = new Position();
    map.addControl(position);
    map.addEventListener("mousemove", (event) => {
      let lat = Math.round(event.latlng.lat * 100000) / 100000;
      let lng = Math.round(event.latlng.lng * 100000) / 100000;
      position.updateHTML(lat, lng);
    });
    L.control
      .scale({
        metric: true,
        imperial: true,
        position: "bottomleft",
        maxWidth: 100,
      })
      .addTo(map);

    setMapState(map);
  }, []);

  return (
    <div id="mapMainContainer" style={{ position: "relative" }}>
      <div id="mapid"></div>
    </div>
  );
};

export default LeafletMap;
