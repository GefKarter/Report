/*
Дан массив. Проверить, одинаковые ли элементы в массиве и вывести результат true или false в консоль.
Речь идёт не о двух рядом стоящих одинаковых элементах, а обо всех.
Проверить, все ли элементы в массиве одинаковые.
*/


let arr = [null, null, null, null, null];
let first = arr[0];
let ident = true;

for (let i = 0; i < arr.length; i++) {
    if (arr[i] === first) {
        continue;
    } else {
        ident = false;
        break;
    };
}

console.log(ident);
