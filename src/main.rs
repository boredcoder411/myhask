use myhask::tokenizer::{Token, Tokenizer};

fn main() {
    let code = "fn main(): u8 { rn 0; }";
    let mut tokenizer = Tokenizer::new(code);

    loop {
        let token = tokenizer.next_token();
        println!("{:?}", token);
        if token == Token::EOF {
            break;
        }
    }
}

