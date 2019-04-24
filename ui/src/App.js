import React, { Component } from 'react';
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";
import { BrowserRouter as Router, Route } from 'react-router-dom';
import './App.css';
import People from "./components/People"
import PersonBio from "./components/PersonBio";

const client = new ApolloClient({
  uri: "https://bankofparliamentapi.elliottsmith.now.sh/"
});
class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <Router>
          <div className="container">
            <h1 style={{margin: 'auto', display: 'block'}}>Bank of Parliament</h1>
            <Route exact path="/" component={People} />
            <Route exact path="/person/:name" component={PersonBio} />
          </div>
        </Router>
      </ApolloProvider>
    );
  }
}

export default App;
