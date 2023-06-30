/*
Дан массив. Нужно вывести в консоль количество чётных и нечётных элементов в массиве.
Если в массиве есть нулевой элемент, то он учитывается и выводится отдельно.
При выполнении задания необходимо учесть, что массив может содержать не только числа, но и,
например, знаки, null и так далее.
*/


let arr = [1, 18, 0, NaN, false, 689, 22, 24, 'qwerty', -11659, 7, 0, 0];
let oddCount = 0;
let evenCount = 0;
let zeroCount = 0;

for (let item of arr) {
    if (typeof item == 'number' && item !== NaN) {
        if (item == 0) {
            zeroCount++;
        } else if (item % 2 == 0) {
            evenCount++;
        } else {
            oddCount++;
        };
    } else {
        continue;
    }
};

console.log(oddCount);
console.log(evenCount);
console.log(zeroCount);
