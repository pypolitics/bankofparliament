import React, { Component, Fragment } from 'react'
import { Query } from "react-apollo";
import gql from "graphql-tag";
import PersonSummary from "./PersonSummary";

// const SEARCH = "Jeremy";
const QUERY = gql`{ Person { name title occupation } }`;
// const QUERY = gql`{ usersBySubstring(Jerem) { name title occupation } }`;

export class People extends Component {
  render() {
    return (
      <Fragment>
        <h3>Results</h3>
        <Query query={QUERY}>
        {
          ({loading, error, data}) => {
            if(loading) return <h4>Loading...</h4>
            if(error) console.log(error);
            return <Fragment>
                {
                  data.Person.map(p => (
                    <PersonSummary key={p.name} data={p}/>
                  ))
                }
              </Fragment>;
          }
        }
        </Query>
      </Fragment>
    )
  }
}

export default People
