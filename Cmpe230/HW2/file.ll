; ModuleID = 'advcalc2ir'
declare i32 @printf(i8*, ...)
@print.str = constant [4 x i8] c"%d\0A\00"

define i32 @main() {
	%x = alloca i32
	%y = alloca i32
	%zvalue = alloca i32
	%k = alloca i32
	store i32 3, i32* %x
	store i32 5, i32* %y
	%x0 = load i32, i32* %x
	%x1 = load i32, i32* %y
	%x2 = add i32 1, %x1
	%x3 = mul i32 %x0, %x2
	%x4 = add i32 23, %x3
	store i32 %x4, i32* %zvalue
	%x5 = load i32, i32* %zvalue
	call i32 (i8*, ...) @printf(i8* getelementptr ([4 x i8], [4 x i8]* @print.str, i32 0, i32 0), i32 %x5)
	%x6 = load i32, i32* %x
	%x7 = load i32, i32* %y
	%x8 = sub i32 %x6, %x7
	%x9 = load i32, i32* %zvalue
	%x10 = sub i32 %x8, %x9
	store i32 %x10, i32* %k
	%x11 = load i32, i32* %x
	%x12 = load i32, i32* %y
	%x13 = mul i32 3, %x12
	%x14 = add i32 2, 5
	%x15 = mul i32 1, %x14
	%x16 = mul i32 %x13, %x15
	%x17 = add i32 %x11, %x16
	store i32 %x17, i32* %k
	%x18 = load i32, i32* %k
	%x19 = add i32 %x18, 1
	call i32 (i8*, ...) @printf(i8* getelementptr ([4 x i8], [4 x i8]* @print.str, i32 0, i32 0), i32 %x19)
	ret i32 0
}