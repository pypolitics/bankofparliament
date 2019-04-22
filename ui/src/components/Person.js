import React from 'react'

export default function Person({ data: {name, occupation}}) {
  return <div className="card card-body mb-3">
    <div className="row">
        <div className="col-md-9">
            <h4>{name}</h4>
            <p>{occupation}</p>
        </div>
        <div className="col-md-3">
            <button className="btn btn-secondary">Details</button>
        </div>
    </div>
  </div>
}
