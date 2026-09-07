CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Iinclude
LDFLAGS = -ldl

CORE_SRC = src/main.c src/core/plugin_manager.c src/ui/menu_ui.c
CORE_INC = -Isrc/core -Isrc/ui

BIN = platform
PLUGIN_DIR = plugins_bin

.PHONY: all clean plugins run

all: $(BIN) plugins

$(BIN): $(CORE_SRC)
	$(CC) $(CFLAGS) $(CORE_INC) -o $(BIN) $(CORE_SRC) $(LDFLAGS)

# 将 plugins/<name>/*.c 各自编译为 plugins_bin/<name>.so
plugins: $(PLUGIN_DIR)
	@for dir in plugins/*/; do \
		name=$$(basename $$dir); \
		echo "编译插件: $$name"; \
		$(CC) $(CFLAGS) -fPIC -shared -o $(PLUGIN_DIR)/$$name.so $$dir*.c; \
	done

$(PLUGIN_DIR):
	mkdir -p $(PLUGIN_DIR)

run: all
	./$(BIN) $(PLUGIN_DIR)

clean:
	rm -f $(BIN)
	rm -f $(PLUGIN_DIR)/*.so
