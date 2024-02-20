document
  .getElementById("your-form-id")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from being submitted normally

    console.log("Form submitted");

    var formData = new FormData(this); // Create a FormData object from the form

    // Log the form data for debugging
    for (var pair of formData.entries()) {
      console.log(pair[0] + ": " + pair[1]);
    }

    fetch("/analysis", {
      // Send a POST request to the /analysis route
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text(); // Parse the response as text
      })
      .then((data) => {
        // Handle the response data
        console.log("Response data:", data);
        // Optionally, redirect to the genome summary page or handle the response in another way
      })
      .catch((error) => {
        // Handle any errors
        console.error("Error:", error);
      });
  });

// Function to toggle visibility of elements based on radio button selection
function show(divId) {
  console.log("Attempting to show div:", divId);
  var div = document.getElementById(divId);
  if (div) {
    console.log("Found div:", divId);
    if (div.style.display === "none" || div.style.display === "") {
      console.log("Changing display to block");
      div.style.display = "block";
    } else {
      console.log("Changing display to none");
      div.style.display = "none";
    }
  } else {
    console.error("Div not found:", divId);
  }
}
