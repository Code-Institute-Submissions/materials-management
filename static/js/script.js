var new_items = [[],[],[],[]]
var new_item_name = []
var new_item_qty = []
var new_item_cost = []
var new_item_id = []
var item_id = 0

$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.fixed-action-btn').floatingActionButton();
    $('.modal').modal();
    $('select').formSelect();
    $('.dropdown-trigger').dropdown();
    $('.tabs').tabs();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    /* Navigation buttons to go to previous and next page*/
    $(".previous, .previous_mobile").click(function (){
        window.history.back();
        return
    })
    $(".next, .next_mobile").click(function (){
        window.history.forward();
        return
    })
    /* Function to add unit when a product is selected
    from the list of new product */
    $("#product_name").on("change", function(){
        material_id = $("#product_name").val();
        unit = $(`#${material_id}`).val();
        $("#unit").html(unit);
        return
    })
    /* Function to add materials to list when registering new product */
    $('#add_product').click(function(){
        material_id = $("#product_name").val();
        if ( $(`#${material_id}`).val() ){
            unit = $(`#${material_id}`).val();
        }else{
            unit = `"No Supplier Found"`;
        };
        new_items[0][0] = $(`.${material_id}`).html();
        new_items[0][1] = $(`#${material_id}`).next().val();
        new_items[1] = $("#product_qty").val();
        if (new_items[1] == ""){
            return
        };
        new_item_name.push(new_items[0][0]);
        new_item_cost.push(Number(new_items[0][1]));
        new_item_qty.push(Number(new_items[1]));
        new_item_id.push(item_id);
        $('#new_product_items').val(new_item_name);
        $('#new_product_cost').val(new_item_cost);
        $('#new_product_qty').val(new_item_qty);
        $('#new_product_id').val(new_item_id);
        $('#items_list').append(`
            <tbody>
                <tr id=${item_id}>
                    <td>${new_items[0][0]}</td>
                    <td>${new_items[1]} ${unit}</td>
                    <td><strong onclick="delete_item(this)"><i class="fas fa-times"></strong></i></div></td>
                </tr>
            </tbody>
        `);
        product_total();
        item_id++;
        return
    })
    /* Function to add products to list when registering new pack */
    $('#add_pack_product').click(function(){
        new_items[0] = $("#pack_product_name").val().split(",");
        new_items[1] = $("#pack_product_qty").val();
        if (new_items[1] == ""){
            return
        }
        new_item_name.push(new_items[0][0]);
        new_item_cost.push(Number(new_items[0][1]));
        new_item_qty.push(Number(new_items[1]));
        new_item_id.push(item_id);
        $('#new_product_items').val(new_item_name);
        $('#new_product_cost').val(new_item_cost);
        $('#new_product_qty').val(new_item_qty);
        $('#new_product_id').val(new_item_id);
        $('#items_list').append(`
            <tbody>
                <tr id=${item_id}>
                    <td>${new_items[0][0]}</td>
                    <td>${new_items[1]}</td>
                    <td>$${new_items[0][1]}</td>
                    <td>$${(new_items[0][1]*new_items[1]).toFixed(2)}</td>
                    <td><strong onclick="delete_item(this)"><i class="fas fa-times"></strong></i></div></td>
                </tr>
            </tbody>
        `);
        product_total();
        item_id++;
        return
    })
    /* Function to add products to list when registering new pack */
    $("#puo_item_name").on("change", function(){
        new_items[0] = $("#puo_item_name").val().split(",");
        unit = new_items[0][2];
        $("#unit").html(unit);
        return
    })
    /* Function to add unit when a material is selected
    from the list of new purchase */
    $('#add_purchase_item').click(function(){
        new_items[0] = $("#puo_item_name").val().split(",");
        new_items[1] = $("#puo_item_qty").val();
        if (new_items[1] == ""){
            return
        };
        new_item_name.push(new_items[0][0]);
        new_item_cost.push(Number(new_items[0][1]));
        new_item_qty.push(Number(new_items[1]));
        new_item_id.push(item_id);
        $('#new_purchase_items').val(new_item_name);
        $('#new_purchase_cost').val(new_item_cost);
        $('#new_purchase_qty').val(new_item_qty);
        $('#new_purchase_id').val(new_item_id);
        $('#items_list').append(`
            <tbody>
                <tr id=${item_id}>
                    <td>${new_items[0][0]}</td>
                    <td>${new_items[1]} ${new_items[0][2]}</td>
                    <td>$${new_items[0][1]} / ${new_items[0][2]}</td>
                    <td>$${(new_items[0][1]*new_items[1]).toFixed(2)}</td>
                    <td><strong onclick="delete_item(this)"><i class="fas fa-times"></strong></i></div></td>
                </tr>
            </tbody>
        `);
        puo_total();
        item_id++;
        return
    })
})
/* Function to delete item from interactive list when registering new product,
material, order ... */
function delete_item(btn){
    index = new_item_id.indexOf(Number(btn.parentElement.id));
    new_item_name.splice(index, 1);
    new_item_cost.splice(index, 1);
    new_item_qty.splice(index, 1);
    new_item_id.splice(index, 1);
    btn.parentElement.parentElement.remove();
    puo_total();
    return
}
/* Function to sum total of interactive new purchase order list */
function puo_total(){
    var sum = 0;
    for(var i=0; i< new_item_cost.length; i++) {
        sum += new_item_cost[i]*new_item_qty[i];
    }
    $('#puo_total').html(`$ ${sum.toFixed(2)}`);
    $('#new_purchase_total').val(sum);
    return
}
/* Function to sum total of interactive new product list */
function product_total(){
    var sum = 0;
    for(var i=0; i< new_item_cost.length; i++) {
        sum += new_item_cost[i]*new_item_qty[i];
    }
    $('#product_total').html(`$ ${sum.toFixed(2)}`);
    $('#new_product_total').val(sum);
    return
}