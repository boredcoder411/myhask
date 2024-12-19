use std::str::Chars;
use std::iter::Peekable;

#[derive(Debug, PartialEq)]
pub enum Token {
    Fn,
    Main,
    Colon,
    U8,
    LBrace,
    RBrace,
    Rn,
    Number(u8),
    Identifier(String),
    Unknown(char),
    EOF,
}

pub struct Tokenizer<'a> {
    input: Peekable<Chars<'a>>,
}

impl<'a> Tokenizer<'a> {
    pub fn new(input: &'a str) -> Self {
        Tokenizer {
            input: input.chars().peekable(),
        }
    }

    fn consume_whitespace(&mut self) {
        while let Some(&ch) = self.input.peek() {
            if ch.is_whitespace() {
                self.input.next();
            } else {
                break;
            }
        }
    }

    fn parse_identifier(&mut self) -> String {
        let mut identifier = String::new();
        while let Some(&ch) = self.input.peek() {
            if ch.is_alphanumeric() || ch == '_' {
                identifier.push(ch);
                self.input.next();
            } else {
                break;
            }
        }
        identifier
    }

    fn parse_number(&mut self) -> Option<u8> {
        let mut number = String::new();
        while let Some(&ch) = self.input.peek() {
            if ch.is_ascii_digit() {
                number.push(ch);
                self.input.next();
            } else {
                break;
            }
        }
        number.parse().ok()
    }

    pub fn next_token(&mut self) -> Token {
        self.consume_whitespace();

        match self.input.next() {
            Some('f') if self.input.peek() == Some(&'n') => {
                self.input.next(); // Consume 'n'
                Token::Fn
            }
            Some('m') if self.parse_identifier() == "main" => Token::Main,
            Some(':') => Token::Colon,
            Some('u') if self.parse_identifier() == "u8" => Token::U8,
            Some('{') => Token::LBrace,
            Some('}') => Token::RBrace,
            Some('r') if self.parse_identifier() == "rn" => Token::Rn,
            Some(ch) if ch.is_ascii_digit() => {
                let mut num_str = ch.to_string();
                if let Some(num) = self.parse_number() {
                    num_str.push_str(&num.to_string());
                }
                Token::Number(num_str.parse().unwrap())
            }
            Some(ch) if ch.is_alphanumeric() || ch == '_' => {
                let mut identifier = ch.to_string();
                identifier.push_str(&self.parse_identifier());
                Token::Identifier(identifier)
            }
            Some(ch) => Token::Unknown(ch),
            None => Token::EOF,
        }
    }
}

