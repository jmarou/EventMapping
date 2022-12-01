import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Route, Link, useHistory } from "react-router-dom";
import { Navbar, Nav, Container } from "react-bootstrap";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from "@fortawesome/fontawesome-free-brands";
import { faFire, faLandmark } from "@fortawesome/free-solid-svg-icons";

import "./App.css";
import LeafletMap from "./LeafletMap.js";

function App(props) {
  let history = useHistory();
  let [home, setHome] = React.useState(true);

  return (
    // React Fragment lets us group a list of children without adding extra nodes to the DOM
    <React.Fragment>
      <div id="mainContainer">
        <Navbar variant="dark" expand="sm" id="EventMappingNavBar">
          <span id="navbar-logo">
            <img src={require("./Icons/logo.png")} style={{ width: 150 }} />
          </span>
          <span id="navbarContainer">
            <Navbar.Toggle
              aria-controls="basic-navbar-nav"
              style={{ backgroundColor: "DarkRed", color: "white" }}
            />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link
                  className="my-auto"
                  onClick={() =>
                    window.open("https://twitter.com/hellenicpolice", "_blank")
                  }
                >
                  <Link
                    id="Hellenic Police"
                    to="https://twitter.com/hellenicpolice"
                  >
                    <div>
                      <FontAwesomeIcon icon={faLandmark} /> Hellenic Police
                    </div>
                  </Link>
                </Nav.Link>

                <Nav.Link
                  className="my-auto"
                  onClick={() =>
                    // setHome(true);
                    window.open("https://twitter.com/pyrosvestiki", "_blank")
                  }
                >
                  <Link
                    id="Hellenic Police"
                    to="https://twitter.com/pyrosvestiki"
                  >
                    <div>
                      <FontAwesomeIcon icon={faFire} /> Hellenic Fire Department
                    </div>
                  </Link>
                </Nav.Link>

                <Nav.Link
                  className="my-auto"
                  onClick={() => {
                    window.open("https://github.com/jmarou");
                  }}
                >
                  <Link id="GitHub_Page" to="/">
                    <div>
                      <FontAwesomeIcon icon={faGithub} /> GitHub Page
                    </div>
                  </Link>
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </span>
        </Navbar>

        <Container fluid id="internalContainer">
          {<Route path="/" render={() => <LeafletMap />}></Route>}
        </Container>
      </div>

      <div id="footerContainer">
        <p>
          EventMapping is an open-source project developed in the context of the
          course Modern Web Applications {}
          <a
            href="http://mycourses.ntua.gr/course_description/index.php?cidReq=PSTGR1083"
            target="_blank"
          >
            MBA: Engineering - Economics Systems hosted by NTUA & UNIPI
          </a>
        </p>
      </div>
    </React.Fragment>
  );
}

export default App;
