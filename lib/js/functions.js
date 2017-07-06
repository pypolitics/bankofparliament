
$('.alertMe').click(function(e) {

    var name = $(this).text();
    var target = e.currentTarget;

    var valuex = target.getAttribute("data-name")

    // console.log(name)
    console.log(target.getAttribute("data-name"))


    var list = document.getElementById('therow');
      // console.log(list)
      var items = list.childNodes;

      var itemsArr = [];
      for (var i in items) {
      if (items[i].nodeType == 1) { // get rid of the whitespace text nodes
        itemsArr.push(items[i]);
        }
      }

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
          return parseInt(a.dataset.companieshouse) == parseInt(b.dataset.companieshouse)
            ? 0
            : (parseInt(a.dataset.companieshouse) > parseInt(b.dataset.companieshouse) ? 1 : -1);
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
        // console.log(itemsArr[i])
      }

    e.preventDefault();// prevent the default anchor functionality
});

function clickFunction() {
  var input, filter, table, tr, td, i;

  var x = document.getElementsByClassName("toggle");
  var i;

  for (i = 0; i < x.length; i++) {

    if (x[i].style.display == "none") {
        x[i].style.display = "";
      } else {
        x[i].style.display = "none"
      }

    }

  }


// $('.photo').click(function(e) {

//     // var name = $(this).text();
//     var target = e.currentTarget;

//     var valuex = target.getAttribute("data-member");

//     console.log(valuex);


//     var x = document.getElementsByClassName(valuex);

//     for (i = 0; i < x.length; i++) {
//       console.log(x[i]);

//       if (x[i].style.display == "none") {
//         x[i].style.display = "";
//       } else {
//         x[i].style.display = "none"
//       }


//     }

//   })

function expandWidget() {

  // var name = $(this).text();
  // console.log(this)
  // console.log(name)

  // console.log("clicky photo")

  // var input, filter, table, tr, td, i;

  // var x = document.getElementsByClassName("bigWidget");
  // var i;
  // // console.log(x)

  // for (i = 0; i < x.length; i++) {
  //   // console.log(x[i]);


  //   // console.log(x[i].style.display);
  //   if (x[i].style.display == "none") {
  //       x[i].style.display = "";
  //     } else {
  //       x[i].style.display = "none"
  //     }

  //   }

  }

function myFunctionBusiness() {

  var input, filter, table, tr, td, i;

  // columns = document.getElementsByClassName("col");
  // row = document.getElementsByClassName("row")

  input = document.getElementById("myInput3");
  filter = input.value.toLowerCase();

  var x = document.getElementsByClassName("col_business");
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


function myFunction() {

  var input, filter, table, tr, td, i;

  // columns = document.getElementsByClassName("col");
  // row = document.getElementsByClassName("row")

  input = document.getElementById("myInput");
  filter = input.value.toLowerCase();

  var x = document.getElementsByClassName("col");
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
