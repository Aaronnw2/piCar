package org.picar.server;

import static org.picar.server.ChannelRegisterHandler.RegisteryType.PRODUCER;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.netty.channel.Channel;
import io.netty.channel.ChannelHandler.Sharable;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;

@Sharable
public class ChannelRegisterHandler extends SimpleChannelInboundHandler<String> {
	
	private static final Logger LOG = LoggerFactory.getLogger(ChannelRegisterHandler.class);
	
	private final Map<DataType, ChannelPairs> channelRegistry;
	public ChannelRegisterHandler(Map<DataType, ChannelPairs> inChanelList) { this.channelRegistry = inChanelList; }
	
	@Override
	protected void channelRead0(ChannelHandlerContext ctx, String msg) throws Exception {
		String registryString = (String)msg;
		RegisteryType registeringAs = RegisteryType.valueOf(registryString.split(",")[0]);
		DataType dataType = DataType.valueOf(registryString.split(",")[1]);
		ChannelPairs channelPairing = this.channelRegistry.get(dataType);
		if (null == channelPairing) {
			channelPairing = new ChannelPairs();
			channelRegistry.put(dataType, channelPairing);
		}
		if(registeringAs.equals(PRODUCER)) {
			channelPairing.getProducers().add(ctx.channel());
			ctx.pipeline().addLast(new ChannelProducer(channelPairing));
			LOG.info("Registered channel {} as producer for {}", ctx.channel(), dataType);
		} else {
			this.channelRegistry.get(dataType).getConsumers().add(ctx.channel());
			ctx.pipeline().addLast(new ChannelConsumer(channelPairing));
			LOG.info("Registered channel {} as consumer for {}", ctx.channel(), dataType);
		}
		ctx.pipeline().remove(ChannelRegisterHandler.class);
		ctx.pipeline().remove(StringDecoder.class);
	}
	
	public enum DataType {
		MOTOR_DATA,
		CAMERA_DATA,
		DISTANCE_SENSOR_DATA
	}
	
	public enum RegisteryType {
		CONSUMER,
		PRODUCER
	}
	
	public class ChannelPairs {
		private final List<Channel> consumers = new ArrayList<Channel>();
		private final List<Channel> producers = new ArrayList<Channel>();
		public List<Channel> getConsumers() { return consumers; }
		public List<Channel> getProducers() { return producers; }
	}
}
