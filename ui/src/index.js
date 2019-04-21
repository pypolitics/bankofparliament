import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";
// import { Neo4jGraphRenderer } from 'neo4j-graph-renderer';
// import NeoGraph from "./NeoGraph";

// const NEO4J_URI = "bolt://54.226.6.209:39188";
// const NEO4J_URI = "https://54.226.6.209:39188";
// const NEO4J_USER = "neo4j";
// const NEO4J_PASSWORD = "divers-ore-servos";

const client = new ApolloClient({
  uri: "https://api.elliottsmith.now.sh/"
});

const Main = () => (
  // <NeoGraph
  //   width={800}
  //   height={600}
  //   containerId={"id1"}
  //   neo4jUri={NEO4J_URI}
  //   neo4jUser={NEO4J_USER}
  //   neo4jPassword={NEO4J_PASSWORD}
  //   backgroundColor={"#c677a8"}
  //   />
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
);

// const Main = () => (
//   <div>
//      <Neo4jGraphRenderer url={NEO4J_URI} user={NEO4J_USER}
//         password={NEO4J_PASSWORD} query="MATCH (n)-[r]->(m) RETURN n,r,m"/>
//   </div>
// );

ReactDOM.render(<Main />, document.getElementById('root'));
serviceWorker.unregister();