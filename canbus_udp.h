#include "esphome.h"
#include <vector>

struct packet {
  unsigned int can_id;
  char size;
  char data[8];
} __attribute__((packed));
packet p;
// ESP_LOGD("can", "canid: %d, size: %d", can_id, data.size());

int sock;
struct sockaddr_in destination, source;

int canbus_messages = 0;

// ESP_LOGD("lambda", "Sent to %s:%d in %d bytes", "172.16.1.234", 1337,
// n_bytes);
// ::close(sock);

class MyCustomComponent : public Component {
public:
  void setup() override {
    inet_aton("172.16.1.234", &destination.sin_addr.s_addr);

    destination.sin_family = AF_INET;
    destination.sin_port = htons(1337);
  }

  void on_can_to_udp(uint32_t can_id, bool use_extended_id,
                     const std::vector<uint8_t> &data) {
    std::uninitialized_copy(data.begin(), data.end(), (unsigned char *)p.data);

    p.can_id = can_id;
    p.size = data.size();

    int n_bytes = ::sendto(sock, &p, sizeof(p), 0,
                           reinterpret_cast<sockaddr *>(&destination),
                           sizeof(destination));
  }
};
