import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Navbar, Nav, Container, Modal } from "react-bootstrap";
import React from "react";
import { Route, Link, useHistory, Switch } from "react-router-dom";
import LeafletMap from "./LeafletMap.js";
// import axios from "axios";


function App(props) {
  let history = useHistory();
  let [home, setHome] = React.useState(true);

  return (
    // React Fragment lets us group a list of children without adding extra nodes to the DOM
    <React.Fragment>
      <div id="mainContainer">
        <Navbar
          variant="dark"
          expand="sm"
          id="EventMappingNavBar"
        >
          <Container id="navbarContainer">
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
                  <Link id="homelink" to="/">
                    Home
                  </Link>              
                </Nav.Link>
                <Nav.Link
                  className="my-auto"
                  onClick={() => {
                    // alert("Github page: https://github.com/jmarou")
                  }}
                >
                  <Link id="GitHub-Page" to="/">
                      <a href="https://github.com/jmarou" target="_self">GitHub Page</a>
                  </Link>   
                </Nav.Link>                  
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>

        <Container fluid id="internalContainer"> 
            { <Route path="/" render={() => <LeafletMap/>}></Route> }
        </Container>
      </div>

      <div id="footerContainer">
        <p>EventMapping was developed during in the context of course "Network Applications" of M.Sc. Technoeconomics of NTUA </p>
      </div>
    </React.Fragment>
  );
}

export default App;

