import React, { Component, Fragment } from 'react'
import { Query } from "react-apollo";
import gql from "graphql-tag";
import Person from "./Person";

const QUERY = gql`{ Person(first: 10) { name title occupation } }`;

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
                    <Person key={p.name} data={p}/>
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
