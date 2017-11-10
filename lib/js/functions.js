// sort function event

$('.alertMe').click(function(e) {

    // var name = $(this).text();
    var target = e.currentTarget;

    var valuex = target.getAttribute("data-name")

    // console.log(name)
    // console.log(target.getAttribute("data-name"))


    var list = document.getElementById('therow');
      // console.log(list)
      var items = list.childNodes;

      var itemsArr = [];
      for (var i in items) {
      if (items[i].nodeType == 1) { // get rid of the whitespace text nodes
        itemsArr.push(items[i]);
        }
      }

      // console.log("All child nodes of 'therow'")
      // console.log(itemsArr)

      if (valuex === "salary")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.salary) == parseInt(b.dataset.salary) 
            ? 0
            : (parseInt(a.dataset.salary) > parseInt(b.dataset.salary) ? 1 : -1);
          });

      if (valuex === "private")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.privateinc) == parseInt(b.dataset.privateinc) 
            ? 0
            : (parseInt(a.dataset.privateinc) > parseInt(b.dataset.privateinc) ? 1 : -1);
          });

      if (valuex === "rental")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.rental) == parseInt(b.dataset.rental) 
            ? 0
            : (parseInt(a.dataset.rental) > parseInt(b.dataset.rental) ? 1 : -1);
          });

      if (valuex === "income")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.income) == parseInt(b.dataset.income) 
            ? 0
            : (parseInt(a.dataset.income) > parseInt(b.dataset.income) ? 1 : -1);
          });

      if (valuex === "gifts")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.gifts) == parseInt(b.dataset.gifts) 
            ? 0
            : (parseInt(a.dataset.gifts) > parseInt(b.dataset.gifts) ? 1 : -1);
          });
      
      if (valuex === "gifts_outside_uk")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.gifts_outside_uk) == parseInt(b.dataset.gifts_outside_uk) 
            ? 0
            : (parseInt(a.dataset.gifts_outside_uk) > parseInt(b.dataset.gifts_outside_uk) ? 1 : -1);
          });

      if (valuex === "direct_donations")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.direct_donations) == parseInt(b.dataset.direct_donations) 
            ? 0
            : (parseInt(a.dataset.direct_donations) > parseInt(b.dataset.direct_donations) ? 1 : -1);
          });

      if (valuex === "indirect_donations")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.indirect_donations) == parseInt(b.dataset.indirect_donations) 
            ? 0
            : (parseInt(a.dataset.indirect_donations) > parseInt(b.dataset.indirect_donations) ? 1 : -1);
          });

      if (valuex === "visits_outside_uk")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.visits_outside_uk) == parseInt(b.dataset.visits_outside_uk) 
            ? 0
            : (parseInt(a.dataset.visits_outside_uk) > parseInt(b.dataset.visits_outside_uk) ? 1 : -1);
          });

      if (valuex === "freebies")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.freebies) == parseInt(b.dataset.freebies) 
            ? 0
            : (parseInt(a.dataset.freebies) > parseInt(b.dataset.freebies) ? 1 : -1);
          });

      if (valuex === "shareholdings")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.shareholdings) == parseInt(b.dataset.shareholdings) 
            ? 0
            : (parseInt(a.dataset.shareholdings) > parseInt(b.dataset.shareholdings) ? 1 : -1);
          });

      if (valuex === "shareholdings_percent")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.shareholdings_percent) == parseInt(b.dataset.shareholdings_percent) 
            ? 0
            : (parseInt(a.dataset.shareholdings_percent) > parseInt(b.dataset.shareholdings_percent) ? 1 : -1);
          });

      if (valuex === "companieshouse")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.active_appointments) == parseInt(b.dataset.active_appointments)
            ? 0
            : (parseInt(a.dataset.active_appointments) > parseInt(b.dataset.active_appointments) ? 1 : -1);
          });

      if (valuex === "family")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.family) == parseInt(b.dataset.family)
            ? 0
            : (parseInt(a.dataset.family) > parseInt(b.dataset.family) ? 1 : -1);
          });

      if (valuex === "lobbyists")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.lobbyists) == parseInt(b.dataset.lobbyists)
            ? 0
            : (parseInt(a.dataset.lobbyists) > parseInt(b.dataset.lobbyists) ? 1 : -1);
          });

      if (valuex === "property")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.property) == parseInt(b.dataset.property) 
            ? 0
            : (parseInt(a.dataset.property) > parseInt(b.dataset.property) ? 1 : -1);
          });

      if (valuex === "wealth")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.wealth) == parseInt(b.dataset.wealth) 
            ? 0
            : (parseInt(a.dataset.wealth) > parseInt(b.dataset.wealth) ? 1 : -1);
          });

      if (valuex === "miscellaneous")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.miscellaneous) == parseInt(b.dataset.miscellaneous) 
            ? 0
            : (parseInt(a.dataset.miscellaneous) > parseInt(b.dataset.miscellaneous) ? 1 : -1);
          });

      // reverse it and display
      itemsArr.reverse();

      for (i = 0; i < itemsArr.length; ++i) {
        list.appendChild(itemsArr[i]);
        // console.log('---------------------------------')
        // console.log(itemsArr[i])
      }

    e.preventDefault();// prevent the default anchor functionality
});

// toggle view click event
// function toggle_function() {
//   var input, filter, table, tr, td, i;

//   var x = document.getElementsByClassName("toggle");
//   var i;

//   for (i = 0; i < x.length; i++) {

//     if (x[i].style.display == "none") {
//         x[i].style.display = "";
//       } else {
//         x[i].style.display = "none"
//       }

//     }

//   }

// front page search event
function search_function() {

  var input, filter, table, tr, td, i;

  // get input and convert to lowercase
  input = document.getElementById("search_text");
  filter = input.value.toLowerCase();

  var x = document.getElementsByClassName("thumbnail_widget");
  var i;

  for (i = 0; i < x.length; i++) {

    classes = x[i].className

    if (classes.indexOf(filter) > -1) {
        x[i].style.display = "";
      } else {
        x[i].style.display = "none";
      }
    }

  }

// open hyperlink plotly click event
$('.plotly-graph-div').on('plotly_click', function(event, data){

  // we only store the hyperlink in the customdata field
  // if we add more, will need to ensure im indexing the dict correctly
  var hyperlink = data.points[0]["customdata"];
  console.log(hyperlink);

  // open hyperlink in new window and set focus
  var win = window.open(hyperlink, '_blank');
  win.focus();
});


function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}


$('.thumbnail_picture').click(function(e) {

  var target = e.currentTarget;
  var valuex = target.getAttribute("data-memberid")
  // console.log(valuex);

  var jsonpath = "https://raw.githubusercontent.com/pypolitics/notpolitics/master/lib/data/plots/replace.json";
  jsoncontent = jsonpath.replace("replace", valuex);
  console.log(jsonpath);

  Plotly.d3.json(jsoncontent, function(err, fig) {
    console.log(fig);

    // purge, plot then display in valuex div
    Plotly.purge(valuex);
    Plotly.plot(valuex, fig.data, fig.layout);
    document.getElementById(valuex).style.display='block';
    document.getElementById('fade').style.display='block'
  });

});
