const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
let sortOrder = urlParams.get('sort_order')
function sortTable(n, event) {
    event.preventDefault();
    sort_column = n;
    if(sortOrder === 'desc'){
      sortOrder = 'asc';
    }else{
      sortOrder = 'desc';
    }
    console.log(sortOrder)
    location.href = "/articulos?sort_column="+sort_column+"&sort_order="+sortOrder;
  }
