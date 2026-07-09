document.querySelectorAll(".wishlist-btn").forEach(button => {

    button.addEventListener("click", function (e) {

        e.preventDefault();

        let productId = this.dataset.id;

        fetch(`/wishlist/toggle/${productId}/`)
            .then(response => response.json())
            .then(data => {

                let icon = this.querySelector("i");

                if (data.status === "added") {

                    icon.classList.remove("fa-regular");
                    icon.classList.add("fa-solid");
                    icon.classList.add("text-danger");

                } else {

                    icon.classList.remove("fa-solid");
                    icon.classList.remove("text-danger");
                    icon.classList.add("fa-regular");

                }

                // Navbar badge update
                let badge = document.getElementById("wishlist-count");
                if (badge) {
                    badge.innerText = data.count;
                }

            });

    });

});
document.querySelectorAll(".add-cart-btn").forEach(button => {

    button.addEventListener("click", function (e) {

        e.preventDefault();

        let productId = this.dataset.id;

        fetch(`/cart/ajax-add/${productId}/`)
            .then(response => response.json())
            .then(data => {

                let badge = document.getElementById("cart-count");

                if (badge) {
                    badge.innerHTML = data.count;
                }

            });

    });

});