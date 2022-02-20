import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Navbar, Nav, Container } from "react-bootstrap";
import React from "react";
import { Route, Link, useHistory, Switch } from "react-router-dom";
import LeafletMap from "./LeafletMap.js";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFire, faLandmark } from "@fortawesome/free-solid-svg-icons";
import { faGithub } from "@fortawesome/fontawesome-free-brands";
// import axios from "axios";

function App(props) {
  let history = useHistory();
  let [home, setHome] = React.useState(true);

  return (
    // React Fragment lets us group a list of children without adding extra nodes to the DOM
    <React.Fragment>
      <div id="mainContainer">
        <Navbar variant="dark" expand="sm" id="EventMappingNavBar">
          <Container id="navbarContainer">
            <Navbar.Toggle
              aria-controls="basic-navbar-nav"
              style={{ backgroundColor: "DarkRed", color: "White" }}
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
          </Container>
        </Navbar>

        <Container fluid id="internalContainer">
          {<Route path="/" render={() => <LeafletMap />}></Route>}
        </Container>
      </div>

      <div id="footerContainer">
        <p>
          EventMapping was developed during in the context of course "Network
          Applications" of{" "}
          <a
            href="http://mycourses.ntua.gr/course_description/index.php?cidReq=PSTGR1083"
            target="_blank"
          >
            M.Sc. Technoeconomics of NTUA
          </a>
        </p>
      </div>
    </React.Fragment>
  );
}

export default App;
