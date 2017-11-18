// sort function event

$('.sort_event').click(function(e) {
    var target = e.currentTarget;
    var valuex = target.getAttribute("data-name");
    var list = document.getElementById('therow');

      var items = list.childNodes;
      var found = false;

      var itemsArr = [];
      for (var i in items) {
      if (items[i].nodeType == 1) { // get rid of the whitespace text nodes
        itemsArr.push(items[i]);
        }
      }

      if (valuex === "salary")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.salary) == parseInt(b.dataset.salary)
            ? 0
            : (parseInt(a.dataset.salary) > parseInt(b.dataset.salary) ? 1 : -1);
          });

      if (valuex === "private")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.privateinc) == parseInt(b.dataset.privateinc)
            ? 0
            : (parseInt(a.dataset.privateinc) > parseInt(b.dataset.privateinc) ? 1 : -1);
          });

      if (valuex === "rental")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.rental) == parseInt(b.dataset.rental)
            ? 0
            : (parseInt(a.dataset.rental) > parseInt(b.dataset.rental) ? 1 : -1);
          });

      if (valuex === "income")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.income) == parseInt(b.dataset.income)
            ? 0
            : (parseInt(a.dataset.income) > parseInt(b.dataset.income) ? 1 : -1);
          });

      if (valuex === "gifts")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.gifts) == parseInt(b.dataset.gifts)
            ? 0
            : (parseInt(a.dataset.gifts) > parseInt(b.dataset.gifts) ? 1 : -1);
          });

      if (valuex === "gifts_outside")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.gifts_outside) == parseInt(b.dataset.gifts_outside)
            ? 0
            : (parseInt(a.dataset.gifts_outside) > parseInt(b.dataset.gifts_outside) ? 1 : -1);
          });

      if (valuex === "direct")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.direct) == parseInt(b.dataset.direct)
            ? 0
            : (parseInt(a.dataset.direct) > parseInt(b.dataset.direct) ? 1 : -1);
          });

      if (valuex === "indirect")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.indirect) == parseInt(b.dataset.indirect)
            ? 0
            : (parseInt(a.dataset.indirect) > parseInt(b.dataset.indirect) ? 1 : -1);
          });

      if (valuex === "visits")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.visits) == parseInt(b.dataset.visits)
            ? 0
            : (parseInt(a.dataset.visits) > parseInt(b.dataset.visits) ? 1 : -1);
          });

      if (valuex === "freebies")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.freebies) == parseInt(b.dataset.freebies)
            ? 0
            : (parseInt(a.dataset.freebies) > parseInt(b.dataset.freebies) ? 1 : -1);
          });

      if (valuex === "shareholdings")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.shareholdings) == parseInt(b.dataset.shareholdings)
            ? 0
            : (parseInt(a.dataset.shareholdings) > parseInt(b.dataset.shareholdings) ? 1 : -1);
          });

      if (valuex === "shareholdings_percent")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.shareholdings_percent) == parseInt(b.dataset.shareholdings_percent)
            ? 0
            : (parseInt(a.dataset.shareholdings_percent) > parseInt(b.dataset.shareholdings_percent) ? 1 : -1);
          });

      if (valuex === "property")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.property) == parseInt(b.dataset.property)
            ? 0
            : (parseInt(a.dataset.property) > parseInt(b.dataset.property) ? 1 : -1);
          });

      if (valuex === "wealth")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.wealth) == parseInt(b.dataset.wealth)
            ? 0
            : (parseInt(a.dataset.wealth) > parseInt(b.dataset.wealth) ? 1 : -1);
          });

      if (valuex === "misc")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.misc) == parseInt(b.dataset.misc)
            ? 0
            : (parseInt(a.dataset.misc) > parseInt(b.dataset.misc) ? 1 : -1);
          });

      if (valuex === "family")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.family) == parseInt(b.dataset.family)
            ? 0
            : (parseInt(a.dataset.family) > parseInt(b.dataset.family) ? 1 : -1);
          });
      if (valuex === "lobbyists")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.lobbyists) == parseInt(b.dataset.lobbyists)
            ? 0
            : (parseInt(a.dataset.lobbyists) > parseInt(b.dataset.lobbyists) ? 1 : -1);
          });

      if (valuex === "expenses")

         // sort function
        itemsArr.sort(function(a, b) {
          found = true;
          return parseInt(a.dataset.expenses) == parseInt(b.dataset.expenses)
            ? 0
            : (parseInt(a.dataset.expenses) > parseInt(b.dataset.expenses) ? 1 : -1);
          });


      console.log(found);
      if (found) {
        console.log(valuex);
        // reverse it and display
        itemsArr.reverse();
        console.log(itemsArr);

        for (i = 0; i < itemsArr.length; ++i) {
          list.appendChild(itemsArr[i]);
        }
      }

    e.preventDefault();// prevent the default anchor functionality
});

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

  if(hyperlink) {
    // open hyperlink in new window and set focus
    var win = window.open(hyperlink, '_blank');
    win.focus();
  };

});

$('.thumbnail_detail').mouseover(function(e) {
    var target = e.currentTarget;
    target.style.opacity='1';
  });

$('.thumbnail_detail').mouseleave(function(e) {
    var target = e.currentTarget;
    target.style.opacity='0';
  });

$('.thumbnail_detail').click(function(e) {

  var target = e.currentTarget;
  var valuex = target.getAttribute("data-memberid")
  document.getElementById(valuex).style.display='block';
  document.getElementById('fade').style.display='block';
  document.getElementById('fade').setAttribute('data-current', valuex);

  var jsonpath = "https://raw.githubusercontent.com/pypolitics/notpolitics/master/lib/data/plots/replace.json";
  jsoncontent = jsonpath.replace("replace", valuex);
  console.log(jsoncontent);

  Plotly.d3.json(jsoncontent, function(err, fig) {

    // purge, plot then display in valuex div
    Plotly.purge(valuex);
    Plotly.plot(valuex, fig.data, fig.layout);
  });

});

$("#fade").on('click', function(e){
  var target = e.currentTarget;
  console.log(target);
  var valuex = target.getAttribute("data-current");
  console.log(valuex);
  document.getElementById(valuex).style.display='none';
  document.getElementById('fade').style.display='none';
});
