from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    print("Serving Ink & Iron site at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()
