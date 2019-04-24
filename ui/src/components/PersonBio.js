import React, { Component, Fragment } from 'react'
import gql from "graphql-tag";
import { Query } from "react-apollo";
import { Link } from 'react-router-dom';
// import classNames from 'classnames';

const QUERY = gql`
    query Person($name: String) {
        Person(name: $name, first: 1) {
            name
            occupation
            title
        }
    }
    `;

export class PersonBio extends Component {
  render() {
    let { name } = this.props.match.params;
    return (
      <Fragment>
          <Query query={QUERY} variables={{name}}>
          {
              ({loading, error, data}) => {
                if(loading) return <h4>Loading..</h4>
                if(error) console.log(error);
                const { name, occupation} = data.Person[0];

                return <div>
                    <h2 className="display- my-3">
                        <div className="text-dark">{name}</div>
                    </h2>
                    <h3 className="display- my-3">
                        <div className="text-dark">{occupation}</div>
                    </h3>
                    <h4 className="mb-3">Biography</h4>
                    <h4 className="mb-3">Income</h4>
                    <h4 className="mb-3">Donors</h4>
                    <h4 className="mb-3">Expenses</h4>
                    <h4 className="mb-3">Assets</h4>
                    <Link className="btn btn-secondary" to="/">Back</Link>
                </div>
              }
          }
          </Query>
      </Fragment>
    )
  }
}

export default PersonBio
