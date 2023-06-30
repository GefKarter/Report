/*
Написать функцию, которая принимает на входе любое число (но не больше 1 000), определяет,
является ли оно простым, и выводит простое число или нет. Если введено больше 1 000,
то выводится сообщение, что данные неверны. Обратите внимание на числа 0 и 1.
*/


console.log(`${simpleNumber(null)}`);
console.log(`${simpleNumber(NaN)}`);
console.log(`${simpleNumber(undefined)}`);
console.log(`${simpleNumber('str')}`);
console.log(`${simpleNumber(-5)}`);
console.log(`${simpleNumber(0)}`);
console.log(`${simpleNumber(1)}`);
console.log(`${simpleNumber(1010)}`);
console.log(`${simpleNumber(1000)}`);
console.log(`${simpleNumber(999)}`);
console.log(`${simpleNumber(7)}`);
console.log(`${simpleNumber(3)}`);
console.log(`${simpleNumber(Infinity)}`);

function simpleNumber(input) {
    console.log(input, typeof input);
    if (typeof input != 'number') {
        return `${input} is invalid input`
    } else {
        numInput = +input;
        if (isNaN(numInput)) {
            return 'Can\'t process NaN'
        } else {
            if (numInput <= 0) {
                return 'Less or equal zero'
            } else if (numInput == 1) {
                return 'It\'s a simple number, because it\'s 1'
            } else if (numInput > 1000) {
                return 'Too much'
            } else {
                let arr = [];
                for (let i = 1; i <= numInput; i++) {
                    if (numInput % i == 0) {
                        arr.push(numInput);
                    };
                };
                if (arr.length == 2) {
                    return `${input} is a simple number`
                } else {
                    return `${input} is not a simple number`
                };
            };
        };
    };
};
