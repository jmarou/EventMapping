import axios from "axios";
import React, { useEffect, useState } from "react";
import { renderToString } from "react-dom/server";
import { useHistory } from "react-router-dom";
import "leaflet-easybutton";

import "./App.css";
import blueIconpng from "./Icons/blueIcon.png";
import redIconpng from "./Icons/redIcon.png";

// This line takes leaflet from the index.html declaration
let L = window.L;

let LeafletMap = (props) => {
  // let history = useHistory();
  let [map, setMap] = useState([]);
  let [police_tweets, setPolice_tweets] = useState();
  let [pyrosvestiki_tweets, setPyrosvestiki_tweets] = useState();



  function addBasemaps(map) {
    const OpenStreetMap = L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
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

    const TonerMap = L.tileLayer(
      "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
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

    const WaterColorMap = L.tileLayer(
      "https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.png",
      {
        maxZoom: 20,
        maxNativeZoom: 19,
        attribution:
          'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>',
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

    const basemaps = {
      "OpenStreet Map": OpenStreetMap,
      "Humanitarian Map": HumanitarianMap,
      "Toner Map": TonerMap,
      "OpenTopo Map": OpenTopoMap,
      "Water Color Map": WaterColorMap,
      "Google Satellite": Google_Satellite,
    };
    
    // const overlaymaps = {
    //   "Tweets: Hellenic Fire Department": pyrosvestiki_tweets,
    //   "Tweets: Hellenic Police": police_tweets,
    // };

    // Add the control layer and set Humanitarian Map as default
    L.control.layers(basemaps).addTo(map);
    HumanitarianMap.addTo(map);
  }

  function positionUpdate(map) {
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
  }

  function addMapControls(map, home) {
    L.control.zoom({ position: "topleft" }).addTo(map);

    // map.setMaxBounds(map.getBounds());

    L.easyButton(
      "fa-home",
      function () {
        map.setView([home.lat, home.lng], home.zoom);
      },
      "Initial View"
    ).addTo(map);

    positionUpdate(map);

    L.control
      .scale({
        metric: true,
        imperial: true,
        position: "bottomleft",
        maxWidth: 100,
      })
      .addTo(map);
  }

  function popUpContainer(feature, department) {
    return renderToString(
      <div>
        {department === "Police" ? (
          <h4 style={{ color: "#0e11db" }}>Hellenic Police Tweet</h4>
        ) : (
          <h4 style={{ color: "#ce1c1c" }}>Pyrosvestiki Tweet</h4>
        )}
        {/* <h1><a href="https://twitter.com/pyrosvestiki/status/{feature.properties.id}" Tweet></a></h1> */}
        <p>
          <strong>Id</strong> = {feature.properties.id}
          <hr />
          <strong>Created At</strong> ={" "}
          {Date(feature.properties.created_at).split(" ").slice(0, 5).join(" ")}
          <hr />
          <strong>Location</strong> = [{feature.geometry.coordinates[0]},
          {feature.geometry.coordinates[1]}]
          <hr />
          <strong>Text</strong>
        </p>
      </div>
    );
  }

  useEffect(function mapInitialization() {
    const home = {
      lat: 38.505,
      lng: 23.91,
      zoom: 6.5,
    };

    // Leaflet map creation
    map = new L.map("mapid", { zoomControl: false, cursor: true });
    map.setView([home.lat, home.lng], home.zoom, false);
    addBasemaps(map);
    addMapControls(map, home);
  }, []);

  useEffect(function getLayers () {
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

    axios.get("/getLayer/police_tweets").then(function (response) {
      console.log(response.data);
      police_tweets = L.geoJson(response.data, {
        pointToLayer: function (feature, latlng) {
          return L.marker(latlng, { icon: blueIcon });
        },
        onEachFeature: function (feature, layer, latlng) {
          layer.bindPopup(
            popUpContainer(feature, "Police") + feature.properties.text
          );
        },
      });
      police_tweets.addTo(map);
    });

    axios.get("/getLayer/pyrosvestiki_tweets").then(function (response) {
      console.log(response.data);
      pyrosvestiki_tweets = L.geoJson(response.data, {
        pointToLayer: function (feature, latlng) {
          return L.marker(latlng, { icon: redIcon });
        },
        onEachFeature: function (feature, layer, latlng) {
          layer.bindPopup(
            popUpContainer(feature, "Pyrosvestiki") + feature.properties.text
          );
        },
      });
      pyrosvestiki_tweets.addTo(map);
    });
  }, map);

  //   // TEST
  //   // let testmarker = L.marker([38.2, 23.23])
  //   // .bindPopup(
  //   //   // `<blockquote class="twitter-tweet" data-theme="dark"><p lang="el" dir="ltr">❗Περισσότερα από 67 κιλά κάνναβης κατασχέθηκαν από αστυνομικούς της Διεύθυνσης Αστυνομίας Ορεστιάδας σε παρέβρια περιοχή του Έβρου.<br>👉<a href="https://t.co/K4MkPuiAVI">https://t.co/K4MkPuiAVI</a> <a href="https://t.co/zVLMGR2VCC">pic.twitter.com/zVLMGR2VCC</a></p>&mdash; Ελληνική Αστυνομία (@hellenicpolice) <a href="https://twitter.com/hellenicpolice/status/1494387434112655362?ref_src=twsrc%5Etfw">February 17, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> `
  //   //   `<blockquote class="twitter-tweet"><p lang="el" dir="ltr"><a href="https://twitter.com/hellenicpolice/status/1494387434112655362?ref_src=twsrc%5Etfw">February 17, 2022</a></blockquote>`
  //   // )
  //   // .addTo(map);

  console.log("main JS");

  return (
    <div id="mapMainContainer" style={{ position: "relative" }}>
      <div id="mapid">{map}</div>
    </div>
  );
};

export default LeafletMap;
