---
title: OUPC 2024 Day1のAをAOJで使える全ての言語で解く
tags:
  - 競技プログラミング
private: false
updated_at: '2025-03-16T18:27:24+09:00'
id: dcd2c8dd194cb6ad15d5
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
# 問題
[問題リンク](https://onlinejudge.u-aizu.ac.jp/services/room.html#OUPC2024/problems/A)

# コード
## C
```c
#include <stdio.h>
#include <ctype.h>

int main() {
  int N;
  scanf("%d",&N);
  char S[101];
  scanf("%s",S);
  char ans[101] = {};
  for(int i = 0;i < N;i++){
    if(S[i] == S[0]){
      ans[i] = toupper(S[i]);
    }else{
      ans[i] = S[i];
    }
  }
  printf("%s\n",ans);
}
```

## C++
```cpp
#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>

int main() {
  int N;
  std::cin >> N;
  std::string S;
  std::cin >> S;
  char old_value = S.front(), new_value = std::toupper(S.front());
  std::replace(S.begin(), S.end(), old_value, new_value);
  std::cout << S << std::endl;
}
```

## Java
```java
import java.util.*;
public class Main {
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		int N = sc.nextInt();
		String S = sc.next();
		System.out.println(S.replace(S.substring(0,1),S.substring(0,1).toUpperCase()));
	}
}
```

## Scala
```scala
import scala.io.StdIn

object Main extends App {
  val N = StdIn.readInt()
  val S = StdIn.readLine()
  println(S.replace(S.substring(0, 1), S.substring(0, 1).toUpperCase))
}
```

## Haskell
```
import Data.Char (toUpper)
import qualified Data.Text as T
import qualified Data.Text.IO as TIO

main :: IO ()
main = do
    n <- readLn :: IO Int
    s <- getLine
    let result = T.replace (T.pack [head s]) (T.pack [toUpper (head s)]) (T.pack s)
    TIO.putStrLn result
```

## OCaml
```ocaml
let () =
  let _ = int_of_string (read_line ()) in
  let s = read_line () in
  let x = String.get s 0 in
  let y = Char.uppercase x in
  let ans = String.map (fun c -> if c = x then y else c) s in
  print_endline ans
```

## C#
```csharp
using System;
class Program
{
	static void Main(string[] args)
	{
		int N = int.Parse(Console.ReadLine());
		string S = Console.ReadLine();
		Console.WriteLine(S.Replace(S[0].ToString(), S[0].ToString().ToUpper()));
	}
}
```

## D
```d
import std.stdio;
import std.string;
import std.conv;
void main()
{
	int N = to!int(chomp(readln()));
	string S = chomp(readln());
	writefln("%s", replace(S, S[0].to!string, S[0].to!string.toUpper));
}
```

## Ruby
```rb
N = gets.to_i
S = gets.chomp
puts S.gsub(S[0], S[0].upcase)
```

## Python3
```py
N = int(input())
S = input()
print(S.replace(S[0],S[0].upper()))
```

## PHP
```php
<?php
fscanf(STDIN, "%d", $N);
fscanf(STDIN, "%s", $S);
echo str_replace($S[0], strtoupper($S[0]), $S)."\n";
?>
```
## JavaScript
```js
function Main(input) {
	input = input.split("\n");
	var N = parseInt(input[0], 10);
	var S = input[1];
	console.log('%s',S.replace(new RegExp(S[0], "g"), S[0].toUpperCase()));
}
Main(require("fs").readFileSync("/dev/stdin", "utf8"));
```

## Rust
```rs
use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();
    input.clear();
    io::stdin().read_line(&mut input).unwrap();
    let s = input.trim();
    let from = s.chars().next().unwrap();
    let to = from.to_uppercase().to_string();
    println!("{}", s.replace(from, &to));
}
```

## Go
```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	var N int
	var S string
	fmt.Scanf("%d", &N)
	fmt.Scanf("%s", &S)
	fmt.Printf("%s\n", strings.Replace(S, string(S[0]), strings.ToUpper(string(S[0])), -1))
}
```

## Kotlin
```kotlin
fun main() {
    val N = readLine()!!.toInt()
    val S = readLine()!!.trim()
    println(S.replace(S[0], S[0].uppercaseChar()))
}
```

AOJのKotlinが壊れてそう

# あとがき
AizuOnlineJudgeで使える言語は有名な言語しかないので、AtCoderと比べると楽ですね。
ただ、CEの内容が見えないので、少し古い環境で苦労しました。
