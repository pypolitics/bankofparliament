import React, { Component } from 'react';
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";
import './App.css';
import People from "./components/People"

const client = new ApolloClient({
  uri: "https://bankofparliamentapi.elliottsmith.now.sh/"
});
class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <div className="container">
          <h1 style={{margin: 'auto', display: 'block'}}>Bank of Parliament</h1>
          <People />
        </div>
      </ApolloProvider>
    );
  }
}

export default App;
