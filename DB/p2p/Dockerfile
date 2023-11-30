# Use an official Go runtime as a parent image
FROM golang:1.20

# Set the working directory inside the container
WORKDIR /app

# Copy the source files
COPY . .

# Initialize the Go module and download dependencies
RUN go mod init p2pnetworkservice && go mod tidy

# Build the Go app
RUN go build -o p2p_network_service .
EXPOSE 10000

# Run the binary program produced by `go install`
CMD ["./p2p_network_service"]
