// Дана строка. Необходимо вывести в консоль перевёрнутый вариант. Например, "Hello" -> "olleH".


const str = 'Python I miss u :(';
let reversed = str.split('').reverse().join('');
console.log(reversed);
