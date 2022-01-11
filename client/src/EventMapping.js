import "bootstrap/dist/css/bootstrap.min.css";
import { Col, Row, Navbar, Nav, Container, Form } from "react-bootstrap";
import React from "react";
import axios from "axios";
import { Switch, Route, Link, useHistory } from "react-router-dom";
import LeafletMap from "./LeafletMap.js";


function EventMapping(props) {
//   let history = useHistory();
  let [home, setHome] = React.useState(true);
  
  return (
    <React.Fragment>
      <div id="mainContainer">
        <Navbar
          variant="dark"
          expand="sm"
          id="EventMappingNavBar"
          style={{
            borderBottom: "2px solid black",
            backgroundSize: "cover",
            backgroundColor: "#3681b8",
          }}
        >
          <Container id="navbarContainer">
            <div
              style={{
                display: "block",
                position: "relative",
                left: "20px",
                top: "-5px",
                zIndex: "1000",
                height: "50px",
                marginRight: "50px",
              }}
            >
            </div>

            <Navbar.Toggle
              aria-controls="basic-navbar-nav"
              style={{ backgroundColor: "Black", color: "DarkGray" }}
            />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link
                  className="my-auto"
                  onClick={() => {
                    setHome(true);
                  }}
                >
                  <Link id="homelink" to="/"
                  style={{textDecoration: "None", color: "Black", fontStyle: "italic"}}>
                    Home
                  </Link>                 
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>

        <Container fluid id="internalContainer"> */
            <Route path="/" render={() => <LeafletMap />}></Route>
        </Container>
      </div>

      <div id="footerContainer">
        {[
          0.05, 0.15, 0.15, 0.25, 0.25, 0.35, 0.25, 0.35, 0.25, 0.45, 0.25,
          0.45, 0.55, 0.45, 0.55,
        ].map((opac, idx) => (
          <div
            className={idx % 2 === 0 ? "footergray" : "footerwhite"}
            style={{ opacity: opac }}
          >
            {" "}
          </div>
        ))}
      </div>
    </React.Fragment>
  );
}

export default EventMapping;
