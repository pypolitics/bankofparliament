// sort function event

$('.alertMe').click(function(e) {
    var target = e.currentTarget;
    var valuex = target.getAttribute("data-name");
    console.log(valuex);

    var list = document.getElementById('therow');

      var items = list.childNodes;

      var itemsArr = [];
      for (var i in items) {
      if (items[i].nodeType == 1) { // get rid of the whitespace text nodes
        itemsArr.push(items[i]);
        }
      }

      if (valuex === "income")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.income) == parseInt(b.dataset.income) 
            ? 0
            : (parseInt(a.dataset.income) > parseInt(b.dataset.income) ? 1 : -1);
          });

      if (valuex === "freebies")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.freebies) == parseInt(b.dataset.freebies) 
            ? 0
            : (parseInt(a.dataset.freebies) > parseInt(b.dataset.freebies) ? 1 : -1);
          });

      if (valuex === "wealth")

         // sort function
        itemsArr.sort(function(a, b) {
          return parseInt(a.dataset.wealth) == parseInt(b.dataset.wealth) 
            ? 0
            : (parseInt(a.dataset.wealth) > parseInt(b.dataset.wealth) ? 1 : -1);
          });

      // reverse it and display
      itemsArr.reverse();
      console.log(itemsArr);

      for (i = 0; i < itemsArr.length; ++i) {
        list.appendChild(itemsArr[i]);
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

  // open hyperlink in new window and set focus
  // var win = window.open(hyperlink, '_blank');
  // win.focus();
});

$('.close').click(function(e) {
    var target = e.currentTarget;
    var valuex = target.getAttribute("data-memberid");
    // console.log(valuex);
    document.getElementById(valuex).style.display='none';
    document.getElementById('fade').style.display='none';
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
  document.getElementById('fade').style.display='block'

  var jsonpath = "https://raw.githubusercontent.com/pypolitics/notpolitics/master/lib/data/plots/replace.json";
  jsoncontent = jsonpath.replace("replace", valuex);
  console.log(jsonpath);

  Plotly.d3.json(jsoncontent, function(err, fig) {

    // purge, plot then display in valuex div
    Plotly.purge(valuex);
    Plotly.plot(valuex, fig.data, fig.layout);
  });

});
