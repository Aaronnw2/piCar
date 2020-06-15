package org.picar.server;

import static java.util.concurrent.TimeUnit.SECONDS;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executors;

import org.picar.server.ChannelRegisterHandler.ChannelPairs;
import org.picar.server.ChannelRegisterHandler.DataType;
import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;

public class ServerApp {
    
	private static final Map<DataType, ChannelPairs> channelList = new HashMap<DataType, ChannelPairs>();
	
	public static void main( String[] args ) {
		Logger rootLogger = (Logger) LoggerFactory.getLogger(org.slf4j.Logger.ROOT_LOGGER_NAME);
		rootLogger.setLevel(Level.INFO);
    	EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        Executors.newSingleThreadScheduledExecutor().scheduleAtFixedRate(() -> rootLogger.info("Channels: \n{}", getChannels()),
        		10L, 10L, SECONDS);
        ChannelRegisterHandler serverHandler = new ChannelRegisterHandler(channelList);
        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             .option(ChannelOption.SO_BACKLOG, 100)
             .handler(new LoggingHandler(LogLevel.INFO))
             .childHandler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 public void initChannel(SocketChannel ch) throws Exception {
                     ChannelPipeline p = ch.pipeline();
                     p.addLast(new LoggingHandler(LogLevel.INFO));
                     p.addLast(new StringDecoder());
                     p.addLast(serverHandler);
                 }
             });
            ChannelFuture f = b.bind(8080).sync();
            
            f.channel().closeFuture().sync();
        } catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
            // Shut down all event loops to terminate all threads.
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }

	private static String getChannels() {
		StringBuilder builder = new StringBuilder();
		channelList.keySet().forEach(key -> {
			builder.append("\t" + key + ":\n")
				.append("\t\tProducers: " + channelList.get(key).getProducers() + "\n")
				.append("\t\tConsumers: " + channelList.get(key).getConsumers() + "\n");
		});
		return builder.toString();
	}
}
