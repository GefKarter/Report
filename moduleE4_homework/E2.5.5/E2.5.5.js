// Дан произвольный массив. Необходимо вывести количество элементов массива,
// затем перебрать его и вывести в консоль каждый элемент массива.


let arr = [null, NaN, 777, 'ok', Infinity, 0.99];

console.log('Length of array is', arr.length);

for (let i = 0; i < arr.length; i++) {
    console.log(arr[i])
};
