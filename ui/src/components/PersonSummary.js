import React from 'react'
import { Link } from 'react-router-dom';

export default function PersonSummary({ data: {name, occupation}}) {
  return <div className="card card-body mb-3">
    <div className="row">
        <div className="col-md-9">
            <h4>{name}</h4>
            <p>{occupation}</p>
        </div>
        <div className="col-md-3">
            <Link to={`/person/${name}`} className="btn btn-secondary">Details</Link>
        </div>
    </div>
  </div>
}
