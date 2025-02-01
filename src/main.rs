use proconio::{derive_readable, fastout, input};
use rand::prelude::SmallRng;
use rand::Rng;
use rand_core::SeedableRng;
use std::time::Instant;

const TIME_LIMIT_MS: u128 = 1700;

struct Input {
    n: usize,
    sp: Vec<Point>,
    ip: Vec<Point>,
}

struct Output {
    ps: Vec<Point>,
}

impl Output {
    fn print(&self) {
        println!("{}", self.ps.len());
        for p in &self.ps {
            println!("{} {}", p.x, p.y);
        }
    }
}

#[fastout]
fn main() {
    let mut rng = SeedableRng::seed_from_u64(0);
    let start_time = Instant::now();
    input! {
        n: usize,
        sp: [Point; n],
        ip: [Point; n],
    }
    let input = Input { n, sp, ip };

    solve(&mut rng, start_time, &input);
}

fn solve(rng: &mut SmallRng, start_time: Instant, input: &Input) {
    const MAX_XY: i32 = 100000;

    let mut best_rectangle = Rectangle {
        pbl: Point { x: 0, y: 0 },
        pur: Point { x: MAX_XY, y: MAX_XY },
    };
    let mut best_score = calc_score_for_rectangle(&input.sp, &input.ip, &best_rectangle);
    while start_time.elapsed().as_millis() < TIME_LIMIT_MS {
        let mut l = rng.gen_range(0..=MAX_XY);
        let mut r = rng.gen_range(0..=MAX_XY);
        let mut b = rng.gen_range(0..=MAX_XY);
        let mut t = rng.gen_range(0..=MAX_XY);
        if l > r {
            std::mem::swap(&mut l, &mut r);
        }
        if b > t {
            std::mem::swap(&mut b, &mut t);
        }
        let rectangle = Rectangle {
            pbl: Point { x: l, y: b },
            pur: Point { x: r, y: t },
        };
        let score = calc_score_for_rectangle(&input.sp, &input.ip, &rectangle);
        if score > best_score {
            best_score = score;
            best_rectangle = rectangle;
        }
    }
    let output = Output {
        ps: vec![best_rectangle.pbl, Point::new(best_rectangle.pur.x, best_rectangle.pbl.y), best_rectangle.pur, Point::new(best_rectangle.pbl.x, best_rectangle.pur.y)],
    };

    output.print();
}

#[derive_readable]
#[derive(Copy, Clone, Debug, PartialOrd, PartialEq, Hash, Eq)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }
}

#[derive(Copy, Clone, Debug)]
struct Rectangle {
    pbl: Point,
    pur: Point,
}

impl Rectangle {
    fn contains(&self, p: &Point) -> bool {
        self.pbl.x <= p.x && p.x <= self.pur.x && self.pbl.y <= p.y && p.y <= self.pur.y
    }
}

fn calc_score_for_rectangle(sp: &[Point], ip: &[Point], rectangle: &Rectangle) -> i32 {
    let mut score = 0;
    for i in 0..sp.len() {
        if rectangle.contains(&sp[i]) {
            score += 1;
        }
        if rectangle.contains(&ip[i]) {
            score -= 1;
        }
    }
    score
}
