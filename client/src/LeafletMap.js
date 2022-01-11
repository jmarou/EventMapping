import "leaflet-easybutton";
import axios from "axios";
import React from "react";
import { Col, Row, Navbar, Nav, Container, Form } from "react-bootstrap";
import * as L from "leaflet/dist/leaflet";


let LeafletMap = (props) => {

    React.useEffect(() => {
        const home = {
            lat: 51.505,
            lon: 15.91,
            zoom: 9
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
      
        const Google_Terrain = L.tileLayer(
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
        
        if (document.getElementById("mapid")) {
            document.getElementById("mapid")._leaflet_id = null;

            let map = new L.map("mapid", {zoomControl: false, cursor: true});
            map.setView([home.lat, home.lng], home.zoom, false);
            
            OpenStreetMap.addTo(map);
            const basemaps = {
                OpenStreetMap: OpenStreetMap,
                "Google Terrain": Google_Terrain,
                OpenTopoMap: OpenTopoMap,
            };
            
            L.control.zoom({ position: "topleft" }).addTo(map);
            
            L.easyButton(
                "fa-home",
                function (btn, map) {
                    map.setView([home.lat, home.lng], home.zoom);
                },
                "Initial View"
            ).addTo(map);
        }
    }, []);
        
        // setMapstate(map);

    return(
        <div id="mapMainContainer" style={{ position: "relative" }}>
            <Container fluid>
            <Row>
                <Col xs={4} style={{ backgroundColor: "#404040" }}></Col>
                <Col xs={4} style={{ backgroundColor: "#4d4d4d" }}></Col>
                <Col xs={3} style={{ backgroundColor: "#404040" }}></Col>
                <Col xs={1} style={{ backgroundColor: "#404040" }}></Col>
            </Row>
            </Container>
            <div id="mapid" style={{ height: "100%" }}></div>
        </div>
    );
}

export default LeafletMap;