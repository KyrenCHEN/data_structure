CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -I.

# 核心代码 + 所有 plugins/<任意目录>/*.c，一起编译成一个可执行文件。
# 新增插件目录后，Makefile 不用改，重新 make 就会自动包含进来。
SRC = main.c plugin_registry.c menu_ui.c $(wildcard plugins/*/*.c)
BIN = platform

.PHONY: all run clean

all: $(BIN)

$(BIN): $(SRC)
	$(CC) $(CFLAGS) -o $(BIN) $(SRC)

run: all
	./$(BIN)

clean:
	rm -f $(BIN)
