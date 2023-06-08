var checkbox = document.getElementById("vendor_checkbox");

checkbox.addEventListener('change', function() {
  if (this.checked) {
    $("#vendor_div").show();
  } else {
    $("#vendor_div").hide();
  }
});