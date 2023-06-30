/*
Написать функцию, которая принимает число как аргумент и возвращает функцию,
которая также принимает число как аргумент и возвращает сумму этих двух чисел.
Выведите в консоль результат.
*/


function getSumFunction(a) {
    return function(b) {
        return a + b
    }
};

const sumFunction = getSumFunction(2);

const sum = sumFunction(3)

console.log(sum);
