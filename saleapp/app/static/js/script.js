function updateCartUI(data) {
    let counters = document.getElementsByClassName("cart-counter");
        for (let c of counters){
            c.innerText = data.total_quantity;
        }
        let amounts = document.getElementsByClassName("cart-amount");
        for (let a of amounts){
            a.innerText = data.total_amount.toLocaleString();
        }
}

function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "POST",
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counters = document.getElementsByClassName("cart-counter");
        for (let c of counters){
            c.innerText = data.total_quantity;
        }
    })
}

function updateCart(productId, obj){
    fetch(`/api/carts/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
       updateCartUI(data);
    })
}

function deleteCart(productId, obj){
    if(confirm("Bạn chắc chắn xóa không?") === true){
        fetch(`/api/carts/${productId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            updateCartUI(data);
            document.getElementsById(`cart${productId}`).style.display = "none";
        });
    }
}

function pay(){
    if(confirm("Bạn chắc chắn thanh toán không?") === true){
        fetch("/api/pay",{
            menthod: "post"
        })
    }
}
